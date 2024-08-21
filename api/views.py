from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, \
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

from .models import *
from .serializers import *
from .utils import get_detailed_list
from .filters import *
from . import choices as choices_module
from .pagination import *


class UserUpdateView(UpdateAPIView):
    """
    Updates the currently authenticated user's information.

    Input:
    - Uses the UserSerializer to update user details.

    Functionality:
    - Retrieves the current user from the request and updates their information.

    Output:
    - Returns the updated user information.
    """
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

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


class SavedPostListCreateView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SavedPostReadSerializer
        return SavedPostWriteSerializer

    def get_queryset(self):
        querset = SavedPost.objects.filter(user=self.request.user).select_related("post")
        return querset


class SavedPostUpdateView(UpdateAPIView):
    serializer_class = SavedPostWriteSerializer
    queryset = SavedPost.objects.all()


class SubscribeNewsletter(APIView):
    """
    Subscribes a user to the newsletter.

    Input:
    - Email address in the GET request parameters.

    Functionality:
    - Validates and creates a new newsletter subscription.

    Output:
    - Returns the created subscription details or an error message if email is not provided.
    """
    def post(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if Newsletter.objects.filter(email=email).exists():
            return Response({'error': 'Email is already subscribed.'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'email': email}
        serializer = NewsletterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UnsubscribeNewsletter(APIView):
    """ 
    Unsubscribes a user from the newsletter.

    Input:
    - Email address in the GET request parameters.

    Functionality:
    - Validates and deletes an existing newsletter subscription.

    Output:
    - Returns a success message or an error message if email is not provided or subscription is not found.
    """

    def post(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            subscription = Newsletter.objects.get(email=email)
        except Newsletter.DoesNotExist:
            return Response({'error': 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        subscription.delete()
        return Response({'message': 'Successfully unsubscribed.'}, status=status.HTTP_200_OK)



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
        choice_type = request.GET.get("type")
        if choice_type.lower() == "car_sorting":
            choices = get_detailed_list(s3_directory="sort_cars", list=choices_module.CAR_SORTING)
        elif choice_type.lower() == "car_brands":
            choices = get_detailed_list(s3_directory="car_brands", list=choices_module.CAR_BRANDS)
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
            {'مواصفات وأسعار السيارات': ['car_reviews']}, 
            {'فيديو': ['videos']}, 
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
 
class SectionPostsView(APIView):
   def get(self, request):
       section_name = request.query_params.get('section_name')
       if not section_name:
           return Response({"error": "section_name parameter is required"}, status=400)
       
       sections = {
           'اختيارات المحررين': ['اختيارات المحررين'],
           'أحدث أخبار السيارات': ['جديد الأخبار', 'سيارات 2023', 'سيارات 2024', 'سيارات معدلة', 'معارض عالمية', 'صور رقمية وتجسسية', 'متفرقات', 'فيس لفت', 'سوبر كارز', 'سيارات نادرة', 'ميكانيك', 'نصائح'],
           'تكنولوجيا السيارات': ['سيارات كهربائية', 'القيادة الذاتية', 'تكنولوجيا السيارات', 'تكنولوجيا متقدمة'],
           'مقالات': ['اختيارات المحررين', 'تقارير وبحوث', 'توب 5', 'قوائم عرب جي تي'],
           'وكلاء وبيانات': ['وكلاء وبيانات'],
           'فيديوهات': ['videos'],
           'مراجعات السيارات': ['car_reviews']
       }
       if section_name not in sections:
           raise NotFound("Section not found")
       categories = sections[section_name]
       
       if categories[0] == 'videos':
           posts = Post.objects.filter(post_type='videos').order_by('-publish_date')
       elif categories[0] == 'car_reviews':
           posts = Post.objects.filter(post_type='car_reviews').order_by('-publish_date')
       else:
           posts = Post.objects.filter(Q(category__overlap=categories)).order_by('-publish_date')
       # Pagination
       paginator = PageNumberPagination()
       paginator.page_size = 10 
       paginated_posts = paginator.paginate_queryset(posts, request)
       serializer = PostListSerializer(paginated_posts, many=True)
       return paginator.get_paginated_response(serializer.data)

class QuestionListCreateView(ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionReadSerializer
        return QuestionWriteSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(user=self.request.user)
        return queryset


class QuestionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuestionReadSerializer
        return QuestionWriteSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(user=self.request.user)
        return queryset


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
