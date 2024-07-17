from rest_framework.serializers import ModelSerializer

from .models import *


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = [
            "username",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
        }


class FavoritePresenterSerializer(ModelSerializer):
    
    class Meta:
        model = FavoritePresenter
        fields = "__all__"


class FavoriteShowSerializer(ModelSerializer):
    
    class Meta:
        model = FavoriteShow
        fields = "__all__"


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "tag"]
