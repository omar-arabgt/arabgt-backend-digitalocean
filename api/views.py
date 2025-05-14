import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, RetrieveAPIView, \
    ListCreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.cache import cache

from .models import *
from .serializers import *
from .filters import *
from . import choices as choices_module
from .pagination import *
from .permissions import *


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Retrieves and updates the currently authenticated user's information.

    Input:
    - Uses the UserSerializer to display user details.
    - Uses the UserUpdateSerializer to update user details.

    Functionality:
    - Retrieves the current user from the request and updates their information.

    Output:
    - Returns the user's information or the updated user information.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """
        if self.request.method == 'GET':
            return self.serializer_class
        return UserUpdateSerializer

    def get_object(self):
        """
        Returns the current authenticated user.
        """
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """
        Updates the user's information and optionally subscribes the user to the newsletter.
        Awards points if the user updates their profile.
        """
        subscribe = request.data.pop("subscribe_newsletter", None)
        if subscribe:
            try:
                subscribe_newsletter(request.user.email)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            set_point(request.user.id, PointType.FILL_PROFILE_FIELD.name)

        # we copy same code as super().update and just use different serializer class on response 
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        serializer = self.serializer_class(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete user profile"""
        confirmation = request.data.get('confirmation')
        delete_reason = request.data.get('delete_reason')
        if confirmation != "تأكيد حذف الحساب":
            return Response(
                {'error': 'The confirmation text does not match.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = self.get_object()
        if instance.is_superuser or instance.is_staff:
            return Response({
                'error': 'You cannot delete a superuser or staff member.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete(delete_reason=delete_reason)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class FavoritePresenterListView(ListAPIView):
    """
    Lists all favorite presenters.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves and lists all favorite presenters from the database.

    Output:
    - Returns a list of favorite presenters using the FavoritePresenterSerializer.
    """
    serializer_class = FavoritePresenterSerializer
    queryset = FavoritePresenter.objects.all()


class FavoriteShowListView(ListAPIView):
    """
    Lists all favorite shows.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves and lists all favorite shows from the database.

    Output:
    - Returns a list of favorite shows using the FavoriteShowSerializer.
    """
    serializer_class = FavoriteShowSerializer
    queryset = FavoriteShow.objects.all()


class PostListView(ListAPIView):
    """
    Lists all posts with pagination and filtering.

    Input:
    - Supports filtering via PostFilter and pagination via CustomPagination.

    Functionality:
    - Retrieves and lists all posts, ordered by publish date in descending order.

    Output:
    - Returns a paginated list of posts using the PostListSerializer.
    """
    serializer_class = PostListSerializer
    filterset_class = PostFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title"]
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.GET.get("is_saved"):
            return Post.objects.filter(postaction__is_saved=True, postaction__user=self.request.user.id, is_published=True).order_by("-postaction__saved_at")
        return Post.objects.all().order_by("-publish_date")


class PostRetrieveView(RetrieveAPIView):
    """
    Retrieves a specific post by its ID.

    Input:
    - Post ID in the URL.

    Functionality:
    - Retrieves the details of a specific post.

    Output:
    - Returns the post details using the PostSerializer.
    """
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostActionUpdateView(UpdateAPIView):
    """
    Updates or creates an action related to a post for the authenticated user.

    Input:
    - Post ID passed as a URL parameter.
    - Uses the PostActionSerializer to update the action.

    Functionality:
    - Retrieves the post by ID and updates or creates a related action (like, bookmark, etc.).

    Output:
    - Returns the updated or created PostAction.
    """
    lookup_url_kwarg = "post_id"
    serializer_class = PostActionSerializer

    def get_object(self):
        """
        Retrieves the post by ID and ensures a PostAction object exists for the current user.
        """
        try:
            post = Post.objects.get(id=self.kwargs.get("post_id"), is_published=True)
        except:
            raise Http404
        post_action, _ = PostAction.objects.get_or_create(user=self.request.user, post=post)
        return post_action


class SubscribeNewsletter(APIView):
    """
    Subscribes a user to the newsletter.

    Input:
    - email and unsubscribe in the GET request parameters.

    Functionality:
    - Create or delete a new newsletter subscription.

    Output:
    - Returns success or fail message
    """
    def post(self, request):
        """
        Handles the subscription or unsubscription process for the newsletter.
        """
        email = request.data.get("email") or request.GET.get("email")

        unsubscribe = request.data.get("unsubscribe") or request.GET.get("unsubscribe")

        try:
            if not email:
                raise Exception("Email is required")

            if unsubscribe:
                subscribe_newsletter(email, unsubscribe=True)
            else:
                subscribe_newsletter(email)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("OK")


class ChoicesView(APIView):
    """
    Provides various choice lists based on the requested type.

    Input:
    - Choice type in the GET request parameters (e.g., gender, country, car).

    Functionality:
    - Retrieves and returns the specified choice list.

    Output:
    - Returns the requested choice list or an empty list if the type is not recognized.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieves the requested choice list based on the choice type provided in the query parameters.
        """
        choice_type = request.GET.get("type", "").lower()
        choices = getattr(choices_module, str(choice_type).upper(), [])
        return Response(choices)


class ContactUsView(APIView):
    """
    Handles 'Contact Us' form submissions.

    Input:
    - Name, email, and message content in the POST request data.

    Functionality:
    - Sends an email with the provided contact information and message.

    Output:
    - Returns a success message if the email is sent, or an error message if required fields are missing or email sending fails.
    """
    def send_contact_email(self, name, email, message_content):
        """
        Sends an email to the specified addresses with the contact form details.
        """
        subject = 'Contact Us message From ArabGT Mobile App'
        # DEV ONLY
        # DEV ONLY
        # DEV ONLY
        # DEV ONLY
        # DEV ONLY
        # DEV ONLY
        to_emails = ["info@arabgt.com"]
        context = {
            'name': name,
            'email': email,
            'message_content': message_content
        }
        email_template = 'api/contact_us_email.html'
        email_body = render_to_string(email_template, context)

        mail = EmailMessage(subject, email_body, to=to_emails)
        mail.content_subtype = 'html'
        mail.send()

    def post(self, request):
        """
        Processes the 'Contact Us' form submission and sends an email with the provided details.
        """
        name = request.data.get('name')
        email = request.data.get('email')
        message_content = request.data.get('message_content')

        if not name or not email or not message_content:
            return Response(
                {'error': 'Name, email, and message content are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.send_contact_email(name, email, message_content)
            return Response({'success': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvertisementRequest(APIView):
    """
    Handles 'Advertisement requests' form submissions.

    Input:
    - Name, Company, Email, Phone Number and message content in the POST request data.

    Functionality:
    - Sends an email with the provided contact information and message.

    Output:
    - Returns a success message if the email is sent, or an error message if required fields are missing or email sending fails.
    """
    def send_contact_email(self, name, email, company, phone_number, message_content):
        """
        Sends an email to the specified addresses with the advertisement request details.
        """
        subject = 'Advertisement Requests From ArabGT Mobile App'
        # DEV ONLY
        to_emails = ["info@arabgt.com"]
        context = {
            'name': name,
            'email': email,
            'company': company,
            'phone_number': phone_number,
            'message_content': message_content
        }
        email_template = 'api/advertisement_requests_email.html'
        email_body = render_to_string(email_template, context)

        mail = EmailMessage(subject, email_body, to=to_emails)
        mail.content_subtype = 'html'
        mail.send()

    def post(self, request):
        """
        Processes the advertisement request form submission and sends an email with the provided details.
        """
        name = request.data.get('name')
        company = request.data.get('company')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        message_content = request.data.get('message_content')

        if not name or not email:
            return Response(
                {'error': 'Name, email, and message content are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.send_contact_email(name, email, company, phone_number, message_content)
            return Response({'success': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HomePageView(APIView):
    """
    Retrieves the homepage content, divided into various sections, each containing the latest posts.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves posts for different sections of the homepage, cached for 24 hours.

    Output:
    - Returns the homepage content divided into sections.
    """
    # @method_decorator(cache_page(60 * 60 * 24, key_prefix="home_page_view_cache"))
    def get(self, request):
        """
        Retrieves posts for each section on the homepage, organized by section name.
        """

        # Define sections and whether they are hidden
        sections = [
            {'name': 'اختيارات المحررين', 'categories': ['اختيارات المحررين'], 'is_hidden': False, 'is_dark_theme': False},
            {'name': 'أحدث أخبار السيارات', 'categories': ['جديد الأخبار', 'سيارات 2023', 'سيارات 2024', 'سيارات معدلة', 'معارض عالمية', 'صور رقمية وتجسسية', 'متفرقات', 'فيس لفت', 'سوبر كارز', 'سيارات نادرة', 'ميكانيك', 'نصائح'], 'is_hidden': False, 'is_dark_theme': True},
            {'name': 'تكنولوجيا السيارات', 'categories': ['سيارات كهربائية', 'القيادة الذاتية', 'تكنولوجيا السيارات', 'تكنولوجيا متقدمة'], 'is_hidden': False, 'is_dark_theme': False},
            {'name': 'مقالات', 'categories': ['اختيارات المحررين', 'تقارير وبحوث', 'توب 5', 'قوائم عرب جي تي'], 'is_hidden': True, 'is_dark_theme': False},
            {'name': 'وكلاء وبيانات', 'categories': ['وكلاء وبيانات'], 'is_hidden': True, 'is_dark_theme': False},
            {'name': 'فيديوهات', 'categories': ['videos'], 'is_hidden': True, 'is_dark_theme': False},
            {'name': 'مراجعات السيارات', 'categories': ['car_reviews'], 'is_hidden': False, 'is_dark_theme': False},
        ]

        result = []

        for section in sections:
            name = section['name']
            categories = section['categories']
            is_hidden = section['is_hidden']
            is_dark_theme = section['is_dark_theme']

            if is_hidden:
                posts = []  # No query, just empty
            elif categories[0] == 'videos':
                posts = Post.objects.filter(post_type='videos', is_published=True).order_by('-publish_date')[:3]
            elif categories[0] == 'car_reviews':
                posts = Post.objects.filter(post_type='car_reviews', is_published=True).order_by('-publish_date')[:3]
            elif name == 'أحدث أخبار السيارات':
                posts = Post.objects.filter(Q(category__overlap=categories), is_published=True).order_by('-publish_date')[:6]
            else:
                posts = Post.objects.filter(Q(category__overlap=categories), is_published=True).order_by('-publish_date')[:3]

            section_data = {
                'section_name': name,
                'posts': posts,
                'is_hidden': is_hidden,
                'is_dark_theme': is_dark_theme
            }

            result.append(section_data)

        serializer = HomepageSectionSerializer(result, many=True)
        return Response(serializer.data)


class SectionPostsView(ListAPIView):
    """
    Retrieves posts for a specific section with pagination.

    Input:
    - Section name passed as a query parameter.

    Functionality:
    - Retrieves posts related to the section name, with support for pagination.

    Output:
    - Returns a paginated list of posts for the specified section.
    """
    serializer_class = PostListSerializer
    pagination_class = CustomPagination
    page_size = 10

    def get_queryset(self):
        """
        Retrieves the queryset of posts based on the section name provided.
        """
        section_name = self.request.query_params.get("section_name")
        sections = {
            'اختيارات المحررين': ['اختيارات المحررين'],
            'أحدث أخبار السيارات': ['جديد الأخبار', 'سيارات 2023', 'سيارات 2024', 'سيارات معدلة', 'معارض عالمية', 'صور رقمية وتجسسية', 'متفرقات', 'فيس لفت', 'سوبر كارز', 'سيارات نادرة', 'ميكانيك', 'نصائح'],
            'تكنولوجيا السيارات': ['سيارات كهربائية', 'القيادة الذاتية', 'تكنولوجيا السيارات', 'تكنولوجيا متقدمة'],
            'مقالات': ['اختيارات المحررين', 'تقارير وبحوث', 'توب 5', 'قوائم عرب جي تي'],
            'وكلاء وبيانات': ['وكلاء وبيانات'],
            'فيديوهات': ['videos'],
            'مراجعات السيارات': ['car_reviews'],
            'خصيصاً لك': [],  # for you section
        }
        if section_name not in sections:
            raise NotFound("Section not found")

        categories = sections[section_name]
        user = self.request.user

        # if section_name == 'خصيصاً لك':
        #     if not user.is_authenticated:
        #         raise PermissionDenied("You must be logged in to view this section")
        #     favorite_cars_en = [car if car == "BMW" else car.lower() for car in user.favorite_cars]
        #     queryset = Post.objects.filter(Q(tag__overlap=favorite_cars_en) | Q(tag__contains=['اخترنا-لك']))

        if section_name == 'خصيصاً لك':
            if not user.is_authenticated:
                raise PermissionDenied("You must be logged in to view this section")

            SPECIAL_ARABIC_OVERRIDES = {
            "BMW": "بي إم دبليو",
            "Mercedes-Benz": "مرسيدس",
            }
            english_to_arabic = dict(CAR_BRANDS_ITEMS)

            favorite_tags = set()

            for car in user.favorite_cars:
                car_lower = car.lower()

                # Always include the lowercase English name
                if car == "BMW":
                    favorite_tags.add("BMW")
                else:
                    favorite_tags.add(car_lower)

                # Determine Arabic equivalent (override > mapping > skip)
                if car in SPECIAL_ARABIC_OVERRIDES:
                    arabic_name = SPECIAL_ARABIC_OVERRIDES[car]
                elif car in english_to_arabic:
                    arabic_name = english_to_arabic[car]
                else:
                    arabic_name = None

                if arabic_name:
                    favorite_tags.add(normalize_arabic(arabic_name))
            # print(favorite_tags)
                queryset = Post.objects.filter(Q(tag__overlap=list(favorite_tags)) | Q(tag__contains=['اخترنا-لك']), is_published=True)



        elif categories[0] in ["videos", "car_reviews"]:
            queryset = Post.objects.filter(post_type=categories[0], is_published=True)
        else:
            queryset = Post.objects.filter(Q(category__overlap=categories), is_published=True)
        return queryset.order_by("-publish_date")

    def get(self, request, *args, **kwargs):
        """
        Validates the section name parameter and retrieves the list of posts for the specified section.
        """
        section_name = request.query_params.get("section_name")
        if not section_name:
            return Response({"error": "section_name parameter is required"}, status=400)
        return super().get(request, *args, **kwargs)


class QuestionListCreateView(ListCreateAPIView):
    """
    Retrieves and creates questions within a specified forum or group.

    Input:
    - Group ID or Forum ID passed as a query parameter.

    Functionality:
    - Retrieves the list of questions, or creates a new question.

    Output:
    - Returns a list of questions or the created question details.
    """
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["group_id", "forum_id"]
    search_fields = ["content"]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """
        if self.request.method == "GET":
            return QuestionReadSerializer
        return QuestionWriteSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of questions, with optional filtering for pinned questions.
        """
        if self.request.GET.get("is_pinned"):     
            queryset = Question.objects.filter(pinned_by=self.request.user)
        else:
            queryset = Question.objects.all()
        return queryset.prefetch_related("pinned_by").order_by("-created_at")


class QuestionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a specific question.

    Input:
    - Question ID passed as a URL parameter.

    Functionality:
    - Retrieves, updates, or deletes the specified question.

    Output:
    - Returns the question details, or a success message upon update or deletion.
    """
    queryset = Question.objects.all()
    permission_classes = [IsOwnerOrReadOnlyPermission]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """
        if self.request.method == "GET":
            return QuestionDetailSerializer
        return QuestionWriteSerializer

class QuestionReportView(APIView):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        question = get_object_or_404(Question, pk=pk)
        question.report_count = F("report_count") + 1
        question = question.save(update_fields=["report_count"])
        
        question = Question.objects.get(id=pk)
        if question.report_count >= 5:
            question.delete()

        return Response("OK")
    
class PinQuestionView(APIView):
    """
    Pins or unpins a specific question for the authenticated user.

    Input:
    - Question ID passed as a URL parameter.
    - is_pinned flag in the POST request data.

    Functionality:
    - Pins or unpins the question based on the is_pinned flag.

    Output:
    - Returns a success message upon pinning or unpinning.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles the pinning or unpinning of a question based on the provided data.
        """
        is_pinned = request.data.get("is_pinned")

        question = get_object_or_404(Question, id=self.kwargs.get("question_id"))
        if is_pinned:
            question.pinned_by.add(request.user)
        else:
            question.pinned_by.remove(request.user)

        return Response("OK")


class ReplyCreateView(CreateAPIView):
    """
    Creates a new reply to a question.

    Input:
    - Reply content in the POST request data.

    Functionality:
    - Creates a new reply associated with a question.

    Output:
    - Returns the created reply details.
    """
    serializer_class = ReplyWriteSerializer


class ReplyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a specific reply.

    Input:
    - Reply ID passed as a URL parameter.

    Functionality:
    - Retrieves, updates, or deletes the specified reply.

    Output:
    - Returns the reply details, or a success message upon update or deletion.
    """
    queryset = Reply.objects.all()
    permission_classes = [IsOwnerOrReadOnlyPermission]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method.
        """
        if self.request.method == "GET":
            return ReplyReadSerializer
        return ReplyWriteSerializer


class MobileReleaseView(APIView):
    """
    Retrieves the latest mobile release version for the specified platform.
    If the user's version is the latest, returns is_uptodate=True.
    """
    serializer_class = MobileReleaseSerializer  # Optional, for clarity

    def get(self, request, *args, **kwargs):
        platform = self.request.GET.get("platform", "")
        try:
            version_number = int(self.request.GET.get("version_number", 0))
        except ValueError:
            version_number = 0

        latest_release = MobileRelease.objects.filter(
            platform=platform
        ).order_by("-version_number").first()

        if latest_release is None:
            return Response(
                {"detail": "No releases found for this platform."},
                status=status.HTTP_404_NOT_FOUND
            )

        is_uptodate = version_number >= latest_release.version_number

        release_data = None
        if not is_uptodate:
            release_data = MobileReleaseSerializer(latest_release).data

        return Response({
            "is_uptodate": is_uptodate,
            "release": release_data
        })


class NotificationList(ListAPIView):
    """
    Lists all notifications for the authenticated user.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves and lists all notifications for the current user.

    Output:
    - Returns a list of notifications using the NotificationSerializer.
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Retrieves the queryset of notifications for the current authenticated user.
        """
        queryset = Notification.objects.filter(user=self.request.user).order_by("-created_at")
        return queryset


class ForumListView(ListAPIView):
    """
    Lists all forums available in the application.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves and lists all forums from the database.

    Output:
    - Returns a list of forums using the ForumSerializer.
    """
    serializer_class = ForumSerializer
    queryset = Forum.objects.filter(is_active=True)


class SetPointView(APIView):
    """
    Awards points to the authenticated user based on a specific point type.

    Input:
    - Point type in the POST request data.

    Functionality:
    - Awards points to the user if the point type is valid.

    Output:
    - Returns a success message upon awarding points.
    """

    def post(self, request, *args, **kwargs):
        """
        Validates the point type and awards points to the user.
        """
        point_types = PointType.get_api_points()
        point_type = str(request.data.get("point_type")).upper()
        
        if point_type not in point_types:
            return Response({"error": _(f"point_type is not correct. Choices: {point_types}")}, status=status.HTTP_400_BAD_REQUEST)
        
        set_point(request.user.id, point_type)
        point = User.objects.get(id=request.user.id).point
        return Response({"point": point})


class VerifyOTP(APIView):
    """
    Handles sending and verifying OTP via Twilio Verify API.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if not phone_number:
            return Response({"error": "phone_number cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if otp:
                # Step 2: Check code
                if check_otp_code(phone_number, str(otp)):
                    user.phone_number = phone_number
                    user.save(update_fields=["phone_number"])
                    return Response("OK")
                else:
                    return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Step 1: Send code
                send_otp_code(phone_number)
                return Response("OK")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GroupListView(ListAPIView):
    """
    Lists all active groups with search functionality.

    Input:
    - search (optional): Search query parameter to filter groups
      Example: /api/groups/?search=example

    Functionality:
    - Retrieves and lists all active groups from the database
    - Filters groups based on search query if provided
    - Performs case-insensitive partial matching on name and description fields

    Output:
    - Returns a filtered list of active groups using the GroupSerializer
    """
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Group.objects.filter(is_active=True)
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset


class GroupMembershipView(UpdateAPIView):
    """
    Manages the user's membership in a specific group.

    Input:
    - Group ID passed as a URL parameter.
    - Uses the GroupMembershipSerializer to update the membership details.

    Functionality:
    - Retrieves the specified group and creates or updates the user's membership in that group.

    Output:
    - Returns the updated or created GroupMembership object.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GroupMembershipSerializer
    lookup_url_kwarg = "post_id"

    def get_object(self):
        """
        Retrieves the group by ID and ensures a GroupMembership object exists for the current user.
        If the group is not found or is inactive, raises a 404 error.
        """
        group_id = self.kwargs.get("group_id")
        user = self.request.user

        try:
            group = Group.objects.get(id=group_id, is_active=True)
        except Group.DoesNotExist:
            raise Http404

        obj, _ = GroupMembership.objects.get_or_create(user=user, group=group)
        return obj


class ReactionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReactionSerializer


class ReactionDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        content_type = self.kwargs.get("content_type")
        object_id = self.kwargs.get("object_id")
        try:
            content_type_model = ContentType.objects.get(model=content_type)
            reaction = Reaction.objects.get(user=self.request.user, content_type=content_type_model, object_id=object_id)
        except (Reaction.DoesNotExist, ContentType.DoesNotExist):
            raise Http404
        return reaction


class FileDestroyView(DestroyAPIView):
    queryset = File.objects.all()
    permission_classes = [IsOwnerOfFile]


class FileUploadLimitView(APIView):

    def get(self, *args, **kwargs):
        response = {
            "max_image_size": UPLOAD_MAX_IMAGE_SIZE,
            "max_video_size": UPLOAD_MAX_VIDEO_SIZE,
            "max_image_number": UPLOAD_MAX_IMAGE_NUMBER,
            "max_video_number": UPLOAD_MAX_VIDEO_NUMBER,
            "image_extensions": UPLOAD_IMAGE_EXTENSIONS,
            "video_extensions": UPLOAD_VIDEO_EXTENSIONS,
        }
        return Response(response)



class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"  # Users will be accessed via their ID