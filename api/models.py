from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from .choices import *
from .utils import * 

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
    car_sorting = ArrayField(models.CharField(max_length=30, choices=CAR_SORTING), default=list, blank=True)
    favorite_presenter = models.ForeignKey("FavoritePresenter", blank=True, null=True, on_delete=models.SET_NULL)
    favorite_show = models.ForeignKey("FavoriteShow", blank=True, null=True, on_delete=models.SET_NULL)


    def delete(self, *args, **kwargs):
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
            car_sorting=self.car_sorting,
            favorite_presenter=str(self.favorite_presenter) if self.favorite_presenter else '',
            favorite_show=str(self.favorite_show) if self.favorite_show else '',
        )
        return super().delete(*args, **kwargs)


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
    car_sorting = ArrayField(models.CharField(max_length=30, choices=CAR_SORTING), default=list, blank=True)
    favorite_presenter = models.CharField(max_length=255, blank=True)
    favorite_show = models.CharField(max_length=255, blank=True)


class FavoritePresenter(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)
    video = models.CharField(max_length=255, blank=True)


class FavoriteShow(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)


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


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unsaved=False)


class SavedPost(TimeStampedModel):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    unsaved = models.BooleanField(default=False)

    objects = PostManager()


class Forum(TimeStampedModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="forum")
    is_active = models.BooleanField(default=True)


class Group(TimeStampedModel):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField("User", through="GroupMembership")
    image = models.ImageField(upload_to="group")
    is_active = models.BooleanField(default=True)


class GroupMembership(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "group")


class Question(TimeStampedModel):
    user = models.ForeignKey("User", related_name="questions", on_delete=models.CASCADE)
    forum = models.ForeignKey("Forum", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey("Group", related_name="questions", blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="question", blank=True, null=True)

    def clean(self):
        check_one_field(self, "forum", "group")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class Reply(TimeStampedModel):
    user = models.ForeignKey("User", related_name="replies", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    parent_reply = models.ForeignKey("Reply", related_name="replies", blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to="reply", blank=True, null=True)

    def clean(self):
        check_one_field(self, "question", "parent_reply")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class Reaction(TimeStampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", blank=True, null=True, related_name='reactions', on_delete=models.CASCADE)
    reply = models.ForeignKey("Reply", blank=True, null=True, related_name='reactions', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=8, choices=ReactionType.choices)

    class Meta:
        unique_together = ("user", "question", "reply")
    
    def clean(self):
        check_one_field(self, "question", "reply")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class MobileRelease(TimeStampedModel):
    platform = models.CharField(choices=MobilePlatform.choices)
    release_type = models.CharField(choices=MobileReleaseType.choices)
    version_number = models.IntegerField()

    def __str__(self):
        return f"{self.platform} - {self.version_number}"
