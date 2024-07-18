from django.db import models
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    post_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    category = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    tag = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    related_articles = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    thumbnail = models.CharField(max_length=255)
    content = models.TextField()