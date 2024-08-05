# from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.conf import settings

from .models import *


class UserSerializer(serializers.ModelSerializer):

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


class FavoritePresenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavoritePresenter
        fields = "__all__"


class FavoriteShowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavoriteShow
        fields = "__all__"




class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "tag", "category", "thumbnail", "id"]



class PostSerializer(serializers.ModelSerializer):
    related_articles = PostListSerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"

class HomepageSectionSerializer(serializers.Serializer):
    section_name = serializers.CharField()
    posts = PostListSerializer(many=True)

class SavedPostReadSerializer(serializers.ModelSerializer):
    post = PostListSerializer()

    class Meta:
        model = SavedPost
        fields = "__all__"


class SavedPostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedPost
        fields = ["post", "unsaved"]

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = validated_data["post"]

        if SavedPost.objects.filter(user=user, post=post_id).exists():
            raise ValidationError("This post is already saved!")

        validated_data["user"] = user
        return super().create(validated_data)

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email', 'created_at']
        read_only_fields = ['created_at']


class QuestionWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["title", "content", "group", "forum", "file"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class QuestionReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class MobileReleaseSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = MobileRelease
        fields = ["platform", "release_type", "download_url", "version_number"]

    def get_download_url(self, obj):
        if obj.platform == MobilePlatform.IOS:
            download_url = settings.IOS_STORE_URL
        elif obj.platform == MobilePlatform.ANDROID:
            download_url = settings.ANDROID_STORE_URL
        return download_url
