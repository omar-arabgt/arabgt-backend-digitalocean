from rest_framework.serializers import ModelSerializer, ValidationError

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



class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "tag", "category", "thumbnail", "id"]


class PostSerializer(ModelSerializer):
    related_articles = PostListSerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"


class SavedPostReadSerializer(ModelSerializer):
    post = PostListSerializer()

    class Meta:
        model = SavedPost
        fields = "__all__"


class SavedPostWriteSerializer(ModelSerializer):

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

class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email', 'created_at']
        read_only_fields = ['created_at']
