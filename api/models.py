from django.db import models


class Post(models.Model):
    post_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    edit_date = models.DateTimeField()
    category = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    content = models.TextField()
