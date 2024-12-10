from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


from .choices import *
from .utils import *
from .tasks import *


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Newsletter(TimeStampedModel):
    email = models.EmailField(unique=True)


class User(TimeStampedModel, AbstractUser):
    nick_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, choices=GENDERS)
    nationality = models.CharField(max_length=2, blank=True, choices=COUNTRIES)
    country = models.CharField(max_length=2, blank=True, choices=COUNTRIES)
    has_business = models.BooleanField(blank=True, null=True)
    has_car = models.BooleanField(blank=True, null=True)
    car_type = models.CharField(max_length=255, blank=True, choices=CARS)
    hobbies = ArrayField(models.CharField(max_length=30, choices=HOBBIES), default=list, blank=True)
    interests = ArrayField(models.CharField(max_length=30, choices=INTERESTS), default=list, blank=True)
    favorite_cars = ArrayField(models.CharField(max_length=30, choices=CAR_BRANDS_ITEMS), default=list, blank=True)
    car_sorting = ArrayField(models.CharField(max_length=30, choices=CAR_SORTING_ITEMS), default=list, blank=True)
    favorite_presenter = models.ForeignKey("FavoritePresenter", blank=True, null=True, on_delete=models.SET_NULL)
    favorite_show = models.ForeignKey("FavoriteShow", blank=True, null=True, on_delete=models.SET_NULL)
    point = models.IntegerField(default=5)
    send_notification = models.BooleanField(default=True)
    profile_photo = models.ImageField(blank=True, null=True)
    is_onboarded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if getattr(self, "userprofilepoint", None):
            userprofilepoint = self.userprofilepoint
        else:
            userprofilepoint = UserProfilePoint(user=self)

        point_fields = UserProfilePoint._meta.get_fields()
        profile_point, _, _, _ = PointType.FILL_PROFILE_FIELD.value
        point = 0

        for point_field in point_fields:
            field = point_field.name
            if not getattr(userprofilepoint, field) and getattr(self, field):
                point += profile_point
                setattr(userprofilepoint, field, True)
        self.point = self.point + point

        super().save(*args, **kwargs)
        userprofilepoint.save()

    def delete(self, delete_reason=None, *args, **kwargs):
        DeletedUser.objects.create(
            user_id=self.id,
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            nick_name=self.nick_name,
            phone_number=self.phone_number,
            birth_date=self.birth_date,
            gender=self.gender,
            nationality=self.nationality,
            country=self.country,
            has_business=self.has_business,
            has_car=self.has_car,
            car_type=self.car_type,
            hobbies=self.hobbies,
            interests=self.interests,
            favorite_cars=self.favorite_cars,
            car_sorting=self.car_sorting,
            favorite_presenter=str(self.favorite_presenter) if self.favorite_presenter else '',
            favorite_show=str(self.favorite_show) if self.favorite_show else '',
            delete_reason=delete_reason,
            point=self.point,
            rank=self.rank,
        )
        return super().delete(*args, **kwargs)

    @property
    def is_verified(self):
        verify_fields = [
            "first_name",
            "last_name",
            "nick_name",
            "birth_date",
            "country",
            "nationality",
            "gender",
            "phone_number",
        ]
        for field in verify_fields:
            if not getattr(self.userprofilepoint, field):
                return False
        return True

    @property
    def rank(self):
        ranks = list(UserRank)
        ranks.reverse()
        for rank in ranks:
            if self.point >= rank.value:
                return rank.name

    @property
    def next_rank_value(self):
        next_rank = UserRank.next_rank_value(self.point)
        return next_rank or self.point


class DeletedUser(TimeStampedModel):
    user_id = models.IntegerField(unique=True)
    email = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    nick_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, choices=GENDERS)
    nationality = models.CharField(max_length=2, blank=True, choices=COUNTRIES)
    country = models.CharField(max_length=2, blank=True, choices=COUNTRIES)
    has_business = models.BooleanField(blank=True, null=True)
    has_car = models.BooleanField(blank=True, null=True)
    car_type = models.CharField(max_length=255, blank=True, choices=CARS)
    hobbies = ArrayField(models.CharField(max_length=30, choices=HOBBIES), default=list, blank=True)
    interests = ArrayField(models.CharField(max_length=30, choices=INTERESTS), default=list, blank=True)
    favorite_cars = ArrayField(models.CharField(max_length=30, choices=CAR_BRANDS_ITEMS), default=list, blank=True)
    car_sorting = ArrayField(models.CharField(max_length=30, choices=CAR_SORTING_ITEMS), default=list, blank=True)
    favorite_presenter = models.CharField(max_length=255, blank=True)
    favorite_show = models.CharField(max_length=255, blank=True)
    delete_reason = models.TextField(blank=True)
    point = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=8, blank=True, null=True)


class UserProfilePoint(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    first_name = models.BooleanField(default=False)
    last_name = models.BooleanField(default=False)
    nick_name = models.BooleanField(default=False)
    birth_date = models.BooleanField(default=False)
    nationality = models.BooleanField(default=False)
    country = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    phone_number = models.BooleanField(default=False)
    favorite_presenter = models.BooleanField(default=False)
    favorite_show = models.BooleanField(default=False)
    hobbies = models.BooleanField(default=False)
    interests = models.BooleanField(default=False)
    favorite_cars = models.BooleanField(default=False)
    car_sorting = models.BooleanField(default=False)
    has_car = models.BooleanField(default=False)
    car_type = models.BooleanField(default=False)


class FavoritePresenter(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="favorite_presenter")
    video = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class FavoriteShow(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="favorite_show")

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    post_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    normalized_title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    category = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    tag = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    related_articles = models.ManyToManyField("Post", blank=True)
    thumbnail = models.CharField(max_length=255)
    content = models.JSONField(default=dict)
    post_type = models.CharField(max_length=255)
    modify_date = models.DateTimeField()


class PostAction(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    is_saved = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    saved_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    shared_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_read = self.is_read
        self._is_shared = self.is_shared
        self._is_saved = self.is_saved

    def save(self, *args, **kwargs):
        point_type = None
        now = datetime.now()

        if not self._is_read and self.is_read:
            self.read_at = now
            point_type = PointType.READ_ARTICLE.name
        if not self._is_shared and self.is_shared:
            self.shared_at = now
            point_type = PointType.SHARE_ARTICLE.name
        if not self._is_saved and self.is_saved:
            self.saved_at = now

        if point_type:
            set_point(self.user_id, point_type)

        super().save(*args, **kwargs)


class Forum(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="forum")
    is_active = models.BooleanField(default=True)


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    members = models.ManyToManyField("User", through="GroupMembership")
    image = models.ImageField(upload_to="group")
    is_active = models.BooleanField(default=True)


class GroupMembership(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "group")

    def save(self, *args, **kwargs):
        if not self.id:
            set_point(self.user_id, PointType.GROUP_MEMBERSHIP.name)
        super().save(*args, **kwargs)


class Question(TimeStampedModel):
    user = models.ForeignKey("User", related_name="questions", on_delete=models.CASCADE)
    forum = models.ForeignKey("Forum", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey("Group", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    file = models.FileField(upload_to="question", blank=True, null=True)
    file_extension = models.CharField(max_length=20, blank=True, null=True)
    pinned_by = models.ManyToManyField("User", related_name="pinned_questions", blank=True)
    report_count = models.IntegerField(default=0)
    reactions = GenericRelation("Reaction")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        set_point(self.user_id, PointType.QUESTION.name)

    @property
    def like_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Reaction.objects.filter(content_type=content_type, object_id=self.id).count()
    
    @property
    def reply_count(self):
        replies = Reply.objects.filter(Q(question=self) | Q(parent_reply__in=self.replies.all()))
        return replies.count()


class Reply(TimeStampedModel):
    user = models.ForeignKey("User", related_name="replies", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    parent_reply = models.ForeignKey("Reply", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="reply", blank=True, null=True)
    file_extension = models.CharField(max_length=20, blank=True, null=True)
    reactions = GenericRelation("Reaction")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        set_point(self.user_id, PointType.REPLY.name)
        if not self.id:
            if self.question:
                model = self.question
                question_id = model.id
                message = _("commented on your post")
            else:
                model = self.parent_reply
                question_id = model.question.id
                message = _("replied your comment")

            content = f"{self.user.first_name} {message}: {self.content}"
            link = f"{settings.APP_URL}/question-details?id={question_id}"
            send_push_notification.delay(model.user_id, None, content, link)

    @property
    def like_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Reaction.objects.filter(content_type=content_type, object_id=self.id).count()

    @property
    def reply_count(self):
        return self.replies.all().count()


class Reaction(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    reaction_type = models.CharField(max_length=8, choices=ReactionType.choices, default=ReactionType.LIKE)

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.id:
            set_point(self.user_id, PointType.REACTION.name)

            model = self.content_type.model
            obj = self.content_object
            message = None
            if model == "question":
                message = _("liked your post")
                question_id = obj.id
            elif model == "reply":
                message = _("liked your comment")
                if obj.question:
                    question_id = obj.question.id
                else:
                    question_id = obj.parent_reply.question.id

            if message:
                link = f"{settings.APP_URL}/question-details?id={question_id}"
                content = f"{self.user.first_name} {message}: {obj.content}"
                send_push_notification.delay(obj.user_id, None, content, link)

        return super().save(*args, **kwargs)


class MobileRelease(TimeStampedModel):
    platform = models.CharField(choices=MobilePlatform.choices)
    release_type = models.CharField(choices=MobileReleaseType.choices)
    version_number = models.IntegerField()

    def __str__(self):
        return f"{self.platform} - {self.version_number}"


class Notification(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_admin_notification = models.BooleanField(default=False)


class AdminNotification(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
