from django.urls import path

from .views import *

urlpatterns = [
    path('posts/', PostView.as_view(), name='post-list'),
    path('posts/<int:id>/', PostView.as_view(), name='post-detail'),
]