from django.urls import path

from .views import *


urlpatterns = [
    path('post/', PostListView.as_view(), name="list-post"),
]