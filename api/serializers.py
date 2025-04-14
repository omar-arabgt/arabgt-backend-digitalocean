# from rest_framework.serializers import ModelSerializer, ValidationError, Serializer
from rest_framework import serializers
from django.conf import settings

from .models import *
from .mixins import *


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

    def validate(self, attrs):
        file = attrs.get("file")
        file_extension = file.name.split(".")[-1].lower()
        file_size = file.size / (1024 * 1024)

        if file_extension in UPLOAD_IMAGE_EXTENSIONS:
            if file_size > UPLOAD_MAX_IMAGE_SIZE:
                raise ValidationError({"error": "حجم الملف كبير جداً تعدى الحد المسموح به"})
            attrs["file_type"] = FileType.IMAGE

        elif file_extension in UPLOAD_VIDEO_EXTENSIONS:
            if file_size > UPLOAD_MAX_VIDEO_SIZE:
                raise ValidationError({"error": "حجم الملف كبير جداً تعدى الحد المسموح به"})
            attrs["file_type"] = FileType.VIDEO

        else:
            raise serializers.ValidationError({"error": "صيغة هذا الملف غير مدعومة"})
        
        return super().validate(attrs)


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
    favorite_shows = FavoriteShowSerializer(many=True)

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
            "favorite_shows",
            "point",
            "rank",
            "is_verified",
            "next_rank_value",
            "send_notification",
            "profile_photo",
            "is_onboarded",
            "has_notification",
            "newsletter",
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
            "favorite_shows",
            "send_notification",
            "profile_photo",
            "is_onboarded",
            "has_notification",
            "newsletter",
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
    is_hidden = serializers.BooleanField()
    is_dark_theme = serializers.BooleanField()


class PostActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostAction
        exclude = ["user", "post"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email', 'created_at']
        read_only_fields = ['created_at']


class ReplyWriteSerializer(FileMixin, serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=True,
        write_only=True,
        default=list,
    )

    class Meta:
        model = Reply
        fields = ["id", "question", "parent_reply", "content", "file"]


class ReplyReadSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = QuestionUserSerializer()
    liked_by = serializers.SerializerMethodField()
    files = FileSerializer(many=True)

    class Meta:
        model = Reply
        fields = [
            "id",
            "user",
            "question",
            "parent_reply",
            "content",
            "files",
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


class QuestionWriteSerializer(FileMixin, serializers.ModelSerializer):
    file = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=True,
        write_only=True,
        default=list,
    )

    class Meta:
        model = Question
        fields = ["id", "content", "group", "forum", "file"]


class QuestionReadSerializer(serializers.ModelSerializer):
    user = QuestionUserSerializer()
    pinned_by = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    files = FileSerializer(many=True)

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
            "files",
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
        fields = ["id", "title", "content", "link", "external_link", "is_admin_notification", "user_first_name", "created_at"]

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



class UserProfileSerializer(serializers.ModelSerializer):
    favorite_presenter = FavoritePresenterSerializer(read_only=True)
    favorite_shows = FavoriteShowSerializer(read_only=True, many=True)
    profile_image = serializers.SerializerMethodField()
    next_rank = serializers.SerializerMethodField()
    country_display = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'nick_name', 
            'country_display',
            'favorite_presenter', 
            'favorite_shows', 
            'hobbies',
            'profile_image',
            'point',
            'rank',
            'next_rank',
            'is_verified'
        )

    def get_profile_image(self, obj):
        if obj.profile_photo:
            return self.context['request'].build_absolute_uri(obj.profile_photo.url)
        return None

    def get_next_rank(self, obj):
        return obj.next_rank_value
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() 
    
    def get_country_display(self, obj):
        return obj.get_country_display()
    
    def get_hobbies(self, obj):
        return [dict(HOBBIES).get(hobby, hobby) for hobby in obj.hobbies]
