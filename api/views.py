from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, ListCreateAPIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import *
from .serializers import *
from .filters import *
from .choices import *
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
        
        if choice_type == "gender":
            choices = GENDERS
        elif choice_type == "country":
            choices = COUNTRIES
        elif choice_type == "car":
            choices = CARS
        else:
            choices = []

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


class HomePageView(ListAPIView):
    serializer_class = PostListSerializer

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        categories = [
            "اختيارات المحررين",
            "أحدث أخبار السيارات",
            "تصفح بحسب ماركة السيارة",
            "تكنولوجيا السيارات",
            "برامج عرب جي تي",
            "مقالات",
            "فيديو",
            "مواصفات وأسعار السيارات",
            "وكلاء وبيانات",      
        ]

        queryset = []
        for category in categories:
            posts = list(Post.objects.filter(category__contains=[category]).order_by("-publish_date")[:3])
            queryset += posts

        return queryset
