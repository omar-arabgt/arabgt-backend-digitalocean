from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView

from .models import *
from .serializers import *
from .filters import *
from .choices import *


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
    queryset = Post.objects.all()
    filterset_class = PostFilter


class PostRetrieveView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


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
