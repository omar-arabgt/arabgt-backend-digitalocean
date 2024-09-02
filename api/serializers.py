# from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.conf import settings

from .models import *
from .choices import MobilePlatform, CAR_SORTING, CAR_BRANDS
from .utils import get_detailed_list


class UserSerializer(serializers.ModelSerializer):
    car_sorting = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    car_type = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    favorite_cars = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "nick_name",
            "phone_number",
            "birth_date",
            "gender",
            "nationality",
            "country",
            "has_business",
            "has_car",
            "car_type",
            "hobbies",
            "interests",
            "favorite_cars",
            "car_sorting",
            "favorite_presenter",
            "favorite_show",
            "point",
            "rank",
        ]

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
        return get_detailed_list(obj.favorite_cars, s3_directory="sort_cars", list=CAR_SORTING)

    def get_favorite_cars(self, obj):
        return get_detailed_list(obj.favorite_cars, s3_directory="car_brand", list=CAR_BRANDS)
    
    def get_rank(self, obj):
        ranks = list(UserRank)
        ranks.reverse()
        for rank in ranks:
            if obj.point >= rank.value:
                return rank.name


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "nick_name",
            "phone_number",
            "birth_date",
            "gender",
            "nationality",
            "country",
            "has_business",
            "has_car",
            "car_type",
            "hobbies",
            "interests",
            "favorite_cars",
            "car_sorting",
            "favorite_presenter",
            "favorite_show",
        ]


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
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_is_saved(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            saved_post = PostAction.objects.filter(post_id=obj.id, user_id=user.id, is_saved=True)
            return saved_post.exists()
        return False


class HomepageSectionSerializer(serializers.Serializer):
    section_name = serializers.CharField()
    posts = PostListSerializer(many=True)


class PostActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostAction
        exclude = ["user", "post"]


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


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ["members"]


class GroupMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMembership
        fields = ["is_active"]
