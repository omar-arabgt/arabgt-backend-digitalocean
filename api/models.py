from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

from .choices import *


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
    hobbies = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    favorite_presenter = models.ForeignKey("FavoritePresenter", blank=True, null=True, on_delete=models.SET_NULL)
    favorite_show = models.ForeignKey("FavoriteShow", blank=True, null=True, on_delete=models.SET_NULL)

class DeletedUser(models.Model):
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
    hobbies = ArrayField(models.CharField(max_length=255), default=list, blank=True)
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
    content = models.TextField()


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unsaved=False)


class SavedPost(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unsaved = models.BooleanField(default=False)

    objects = PostManager()
