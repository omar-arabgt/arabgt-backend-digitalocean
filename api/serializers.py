# from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.conf import settings

from .models import *


class FavoritePresenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavoritePresenter
        fields = "__all__"


class FavoriteShowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FavoriteShow
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    car_sorting = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    nationality = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    car_type = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    favorite_cars = serializers.SerializerMethodField()
    favorite_presenter = FavoritePresenterSerializer()
    favorite_show = FavoriteShowSerializer()

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
            "is_verified",
            "next_rank_value",
            "send_notification",
            "profile_photo",
            "is_onboarded",
        ]

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_nationality(self, obj):
        return obj.get_nationality_display()

    def get_country(self, obj):
        return obj.get_country_display()

    def get_car_type(self, obj):
        return obj.get_car_type_display()

    def get_hobbies(self, obj):
        return [dict(HOBBIES).get(hobby) for hobby in obj.hobbies] if obj.hobbies else []

    def get_interests(self, obj):
        return [dict(INTERESTS).get(interest) for interest in obj.interests] if obj.interests else []

    def get_car_sorting(self, obj):
        return [CAR_SORTING_DICT[key] for key in obj.car_sorting] if obj.car_sorting else []

    def get_favorite_cars(self, obj):
        return [CAR_BRAND_DICT[key] for key in obj.favorite_cars] if obj.favorite_cars else []


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
            "send_notification",
            "profile_photo",
            "is_onboarded",
        ]


class QuestionUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "nick_name",
            "point",
            "rank",
            "is_verified",
            "profile_photo",
        ]


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


class ReplyWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ["question", "parent_reply", "content", "file"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        file = validated_data.get("file")
        if file:
            validated_data["file_extension"] = file.name.split(".")[-1].lower()
        return super().create(validated_data)


class ReplyReadSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = QuestionUserSerializer()
    liked_by = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = [
            "id",
            "user",
            "question",
            "parent_reply",
            "content",
            "file",
            "file_extension",
            "file_type",
            "replies",
            "like_count",
            "reply_count",
            "liked_by",
            "created_at",
            "updated_at",
        ]

    def get_replies(self, obj):
        if obj.replies:
            return ReplyReadSerializer(obj.replies.all(), many=True, context=self.context).data
        return None

    def get_liked_by(self, obj):
        user = self.context["request"].user
        content_type = ContentType.objects.get_for_model(self.Meta.model)
        return Reaction.objects.filter(content_type=content_type, object_id=obj.id, user=user).exists()

    def get_file_type(self, obj):
        # TODO: add all required formats
        if obj.file_extension in ["jpg", "jpeg", "png", "webp"]:
            return "image"
        elif obj.file_extension in ["mp4", "mov"]:
            return "video"
        else:
            return None


class QuestionWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["content", "group", "forum", "file"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        file = validated_data.get("file")
        if file:
            validated_data["file_extension"] = file.name.split(".")[-1].lower()
        return super().create(validated_data)


class QuestionReadSerializer(serializers.ModelSerializer):
    user = QuestionUserSerializer()
    pinned_by = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id",
            "user",
            "pinned_by",
            "liked_by",
            "replies",
            "content",
            "group",
            "forum",
            "file",
            "file_extension",
            "file_type",
            "like_count",
            "reply_count",
            "created_at",
            "updated_at",
        ]

    def get_pinned_by(self, obj):
        user = self.context["request"].user
        return user in obj.pinned_by.all()
    
    def get_liked_by(self, obj):
        user = self.context["request"].user
        content_type = ContentType.objects.get_for_model(self.Meta.model)
        return Reaction.objects.filter(content_type=content_type, object_id=obj.id, user=user).exists()

    def get_file_type(self, obj):
        # TODO: add all required formats
        if obj.file_extension in ["jpg", "jpeg", "png", "webp"]:
            return "image"
        elif obj.file_extension in ["mp4", "mov"]:
            return "video"
        else:
            return None


class QuestionDetailSerializer(QuestionReadSerializer):
    replies = ReplyReadSerializer(many=True)


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
    user_first_name = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "title", "content", "link", "is_admin_notification", "user_first_name", "created_at"]

    def get_user_first_name(self, obj):
        return obj.user.first_name


class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Forum
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Group
        exclude = ["members"]

    def get_is_member(self, obj):
        user = self.context["request"].user
        membership = GroupMembership.objects.filter(group=obj, user=user, is_active=True)
        return membership.exists()


class GroupMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMembership
        fields = ["is_active"]


class ReactionSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()

    class Meta:
        model = Reaction
        fields = ["content_type", "object_id"]

    def validate(self, data):
        data = super().validate(data)
        try:
            content_type_model = ContentType.objects.get(model=data["content_type"])
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type")

        model_class = content_type_model.model_class()
        if not model_class.objects.filter(id=data["object_id"]).exists():
            raise serializers.ValidationError("The object with this ID does not exist")

        user = self.context["request"].user
        if self.Meta.model.objects.filter(user=user, content_type=content_type_model, object_id=data['object_id']).exists():
            raise serializers.ValidationError("You have already liked this item.")

        data["content_type"] = content_type_model
        data["user"] = user
        return data
