from django.urls import path

from .views import *


urlpatterns = [
    path('post/', PostListView.as_view(), name="list-post"),
    path('post/fetch-and-process/', FetchAndProcessWpPostsView.as_view(), name='fetch-and-process-posts'),
    path('post/fetch-and-process/<int:post_id>/', FetchAndProcessWpPostByIdView.as_view(), name='fetch-and-process-post-by-id'),
]