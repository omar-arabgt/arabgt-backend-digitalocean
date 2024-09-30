from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

    def save(self, *args, **kwargs):
        created = False
        if not self.id:
            created = True
        super().save(*args, **kwargs)
        if created:
            UserProfilePoint.objects.create(user_id=self.id)

        point_fields = UserProfilePoint._all_fields()
        for field in point_fields:
            if not getattr(self.userprofilepoint, field) and getattr(self, field) is not None:
                set_point.delay(self.id, PointType.FILL_PROFILE_FIELD.name)
                setattr(self.userprofilepoint, field, True)
        self.userprofilepoint.save()

    def delete(self, delete_reason=None, *args, **kwargs):
        DeletedUser.objects.create(
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
        return self.userprofilepoint.is_all_done

    @property
    def rank(self):
        ranks = list(UserRank)
        ranks.reverse()
        for rank in ranks:
            if self.point >= rank.value:
                return rank.name

    @property
    def next_rank_value(self):
        ranks = list(UserRank.__members__)
        index = ranks.index(self.rank)
        next_index = index + 1
        if next_index < len(ranks):
            next_rank = ranks[next_index]
            return UserRank[next_rank].value
        return self.point


class DeletedUser(TimeStampedModel):
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

    @property
    def is_all_done(self):
        fields = self._all_fields()
        for field in fields:
            if not getattr(self, field):
                return False
        return True

    @classmethod
    def _all_fields(cls):
        _fields = cls._meta.get_fields()
        fields = []
        for field in _fields:
            if field.auto_created or field.is_relation:
                continue
            fields.append(field.name)
        return fields


class FavoritePresenter(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="favorite_presenter")
    video = models.CharField(max_length=255, blank=True)


class FavoriteShow(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="favorite_show")


class Post(TimeStampedModel):
    post_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
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

    class Meta:
        unique_together = ("user", "post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_read = self.is_read
        self._is_shared = self.is_shared

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        point_type = None
        if not self._is_read and self.is_read:
            point_type = PointType.READ_ARTICLE.name
        if not self._is_shared and self.is_shared:
            point_type = PointType.SHARE_ARTICLE.name
        if point_type:
            set_point.delay(self.user_id, point_type)


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
            set_point.delay(self.user_id, PointType.GROUP_MEMBERSHIP.name)
        super().save(*args, **kwargs)


class Question(TimeStampedModel):
    user = models.ForeignKey("User", related_name="questions", on_delete=models.CASCADE)
    forum = models.ForeignKey("Forum", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey("Group", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="question", blank=True, null=True)
    pinned_by = models.ManyToManyField("User", related_name="pinned_questions", blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        set_point.delay(self.user_id, PointType.QUESTION.name)

    @property
    def like_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Reaction.objects.filter(content_type=content_type, object_id=self.id).count()


class Reply(TimeStampedModel):
    user = models.ForeignKey("User", related_name="replies", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    parent_reply = models.ForeignKey("Reply", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to="reply", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        set_point.delay(self.user_id, PointType.REPLY.name)
        if not self.id:
            model = self.question or self.parent_reply
            send_push_notification.delay(model.user_id, "title", "content")

    @property
    def like_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Reaction.objects.filter(content_type=content_type, object_id=self.id).count()


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
            set_point.delay(self.user_id, PointType.REACTION.name)
            send_push_notification.delay(self.content_object.user_id, "title", "content")
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
