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
from .utils import get_detailed_list
from .filters import *
from . import choices as choices_module
from .pagination import *


class UserUpdateView(RetrieveUpdateAPIView):
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
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserUpdateSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        subscribe = request.data.pop("subscribe_newsletter", None)
        if subscribe:
            try:
                subscribe_newsletter(request.user.email)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            set_point.delay(request.user.id, PointType.FILL_PROFILE_FIELD.name)
        return super().update(request, *args, **kwargs)


class UserRetrieveView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UserDeleteAPIView(DestroyAPIView):
    """
    Delete a specific user's information.

    Input:
    - User ID is passed in the URL.
    - Confirmation Input that has to be typed before deleting

    Functionality:
    - Retrieves the user by ID and deletes their information.

    Output:
    - Returns a confirmation message upon successful deletion.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.is_superuser or instance.is_staff:
            raise Response({
                'error': 'You cannot delete a superuser or staff member.'},
                status=status.HTTP_403_FORBIDDEN
            )

        instance.delete()

    def delete(self, request, *args, **kwargs):
        confirmation = request.data.get('confirmation')
        if confirmation != "تأكيد حذف الحساب":
            return Response({
                'error': 'The confirmation text does not match.'
            }, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)


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
    queryset = Post.objects.all().order_by('-publish_date')
    filterset_class = PostFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["title"]
    pagination_class = CustomPagination


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
    queryset = Post.objects.all()


class PostActionUpdateView(UpdateAPIView):
    lookup_url_kwarg = "post_id"
    serializer_class = PostActionSerializer

    def get_object(self):
        try:
            post = Post.objects.get(id=self.kwargs.get("post_id"))
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
        email = request.data.get("email")
        unsubscribe = request.data.get("unsubscribe")

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
        choice_type = request.GET.get("type", "").lower()
        
        if choice_type == "car_sorting":
            choices = get_detailed_list(s3_directory="sort_cars", list=choices_module.CAR_SORTING)
        elif choice_type == "car_brands":
            choices = get_detailed_list(s3_directory="car_brand", list=choices_module.CAR_BRANDS)
        else:
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
        subject = 'Contact Us message From ArabGT Mobile App'
        # DEV ONLY
        to_emails = ['basheer@audteye.com', 'zeyad@audteye.com']
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
        subject = 'Advertisement Requests From ArabGT Mobile App'
        # DEV ONLY
        to_emails = ['basheer@audteye.com', 'zeyad@audteye.com']
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
 
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request):
        sections = [
            {'اختيارات المحررين': ['اختيارات المحررين']},
            {'أحدث أخبار السيارات': ['جديد الأخبار', 'سيارات 2023', 'سيارات 2024', 'سيارات معدلة', 'معارض عالمية', 'صور رقمية وتجسسية', 'متفرقات', 'فيس لفت', 'سوبر كارز', 'سيارات نادرة', 'ميكانيك', 'نصائح']},
            {'تكنولوجيا السيارات': ['سيارات كهربائية', 'القيادة الذاتية', 'تكنولوجيا السيارات', 'تكنولوجيا متقدمة']},
            {'مقالات': ['اختيارات المحررين', 'تقارير وبحوث', 'توب 5', 'قوائم عرب جي تي']},
            {'وكلاء وبيانات': ['وكلاء وبيانات']},
            {'فيديوهات': ['videos']},  # post_type videos
            {'مراجعات السيارات': ['car_reviews']}  # post_type car_reviews
        ]

        result = []
        for section in sections:
            section_name = list(section.keys())[0]
            categories = section[section_name]
            if categories[0] == 'videos':
                posts = Post.objects.filter(post_type='videos').order_by('-publish_date')[:3]
            elif categories[0] == 'car_reviews':
                posts = Post.objects.filter(post_type='car_reviews').order_by('-publish_date')[:3]
            else:
                posts = Post.objects.filter(Q(category__overlap=categories)).order_by('-publish_date')[:3]
            
            section_data = {
                'section_name': section_name,
                'posts': posts
            }
            result.append(section_data)

        serializer = HomepageSectionSerializer(result, many=True)
        return Response(serializer.data)
 
class SectionPostsView(ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = CustomPagination
    page_size = 10

    def get_queryset(self):
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

       if section_name == 'خصيصاً لك':
            if not user.is_authenticated:
                raise PermissionDenied("You must be logged in to view this section")
            queryset = Post.objects.filter(tag__overlap=user.favorite_cars)
       elif categories[0] in ["videos", "car_reviews"]:
           queryset = Post.objects.filter(post_type=categories[0])
       else:
           queryset = Post.objects.filter(Q(category__overlap=categories))
       return queryset.order_by("-publish_date")

    def get(self, request, *args, **kwargs):
        section_name = request.query_params.get("section_name")
        if not section_name:
            return Response({"error": "section_name parameter is required"}, status=400)
        return super().get(request, *args, **kwargs)


class QuestionListCreateView(ListCreateAPIView):
    filterset_fields = ["group_id", "forum_id"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionReadSerializer
        return QuestionWriteSerializer

    def get_queryset(self):
        if self.request.GET.get("is_pinned"):     
            queryset = Question.objects.filter(pinned_by=self.request.user)
        else:
            queryset = Question.objects.all()
        return queryset.prefetch_related("pinned_by")


class QuestionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionReadSerializer
        return QuestionWriteSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(user=self.request.user)
        return queryset


class PinQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        is_pinned = request.data.get("is_pinned")

        question = get_object_or_404(Question, id=self.kwargs.get("question_id"))
        if is_pinned:
            question.pinned_by.add(request.user)
        else:
            question.pinned_by.remove(request.user)

        return Response("OK")



class ReplyCreateView(CreateAPIView):
    serializer_class = ReplyWriteSerializer


class ReplyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReplyReadSerializer
        return ReplyWriteSerializer

    def get_queryset(self):
        queryset = Reply.objects.filter(user=self.request.user)
        return queryset


class MobileReleaseView(RetrieveAPIView):
    serializer_class = MobileReleaseSerializer

    def get_object(self):
        platform = self.request.GET.get("platform", "")
        version_number = self.request.GET.get("version_number", 0)
        obj = MobileRelease.objects.filter(platform=platform, version_number__gt=version_number).last()
        return obj


class NotificationList(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset


class ForumListView(ListAPIView):
    serializer_class = ForumSerializer
    queryset = Forum.objects.filter(is_active=True)


class SetPointView(APIView):

    def post(self, request, *args, **kwargs):
        point_types = PointType.get_api_points()
        point_type = str(request.data.get("point_type")).upper()
        
        if point_type not in point_types:
            return Response(_(f"point_type is not correct. Choices: {point_types}"), status=status.HTTP_400_BAD_REQUEST)
        
        set_point.delay(request.user.id, point_type)
        return Response("OK")


class VerifyOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if not phone_number:
            return Response({"error": "phone_number can not be empty!"}, status=status.HTTP_400_BAD_REQUEST)

        CACHE_KEY = f"otp:{user.id}:{phone_number}"

        if otp:
            stored_otp = cache.get(CACHE_KEY)
            if otp == stored_otp:
                cache.delete(CACHE_KEY)
                user.phone_number = phone_number
                user.save(update_fields=["phone_number"])
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            otp = random.randint(1000, 9999)
            body = f"Verification code: {otp}"
            send_sms_notification(phone_number, body)
            cache.set(CACHE_KEY, otp, 180)

        return Response("OK")


class GroupListView(ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.filter(is_active=True)


class GroupMembershipView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupMembershipSerializer
    lookup_url_kwarg = "post_id"
    
    def get_object(self):
        group_id = self.kwargs.get("group_id")
        user = self.request.user

        try:
            group = Group.objects.get(id=group_id, is_active=True)
        except Group.DoesNotExist:
            raise Http404

        obj, _ = GroupMembership.objects.get_or_create(user=user, group=group)
        return obj
