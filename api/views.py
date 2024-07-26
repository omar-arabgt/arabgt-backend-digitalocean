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
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FavoritePresenterListView(ListAPIView):
    serializer_class = FavoritePresenterSerializer
    queryset = FavoritePresenter.objects.all()


class FavoriteShowListView(ListAPIView):
    serializer_class = FavoriteShowSerializer
    queryset = FavoriteShow.objects.all()


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all().order_by('-publish_date')
    filterset_class = PostFilter
    pagination_class = CustomPagination


class PostRetrieveView(RetrieveAPIView):
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


class ChoicesView(APIView):

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
