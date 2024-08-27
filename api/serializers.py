# from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.conf import settings

from .models import *
from .choices import MobilePlatform, CAR_SORTING, CAR_BRANDS


class UserSerializer(serializers.ModelSerializer):
    car_sorting = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    car_type = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    favorite_cars = serializers.SerializerMethodField()

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

    def get_gender(self, obj):
        return obj.get_gender_display() if obj.gender else None

    def get_nationality(self, obj):
        return obj.get_nationality_display() if obj.nationality else None

    def get_country(self, obj):
        return obj.get_country_display() if obj.country else None

    def get_car_type(self, obj):
        return dict(CARS).get(obj.car_type) if obj.car_type else None

    def get_hobbies(self, obj):
        return [dict(HOBBIES).get(hobby) for hobby in obj.hobbies] if obj.hobbies else []

    def get_interests(self, obj):
        return [dict(INTERESTS).get(interest) for interest in obj.interests] if obj.interests else []

    def get_car_sorting(self, obj):
        return [dict(CAR_SORTING).get(car) for car in obj.car_sorting] if obj.car_sorting else []

    def get_favorite_cars(self, obj):
        return [dict(CAR_BRANDS).get(car) for car in obj.favorite_cars] if obj.favorite_cars else []


class UserUpdateSerializer(serializers.ModelSerializer):
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
        fields = ["title", "tag", "category", "thumbnail", "id", "post_type"]



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


class ChildReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = "__all__"


class ReplyWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ["question", "parent_reply", "content", "file"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ReplyReadSerializer(serializers.ModelSerializer):
    replies = ChildReplySerializer(many=True)

    class Meta:
        model = Reply
        fields = "__all__"


class QuestionWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["title", "content", "group", "forum", "file"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class QuestionReadSerializer(serializers.ModelSerializer):
    replies = ReplyReadSerializer(many=True)
    pinned_by = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    def get_pinned_by(self, obj):
        user = self.context["request"].user
        return user in obj.pinned_by.all()


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


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = "__all__"
