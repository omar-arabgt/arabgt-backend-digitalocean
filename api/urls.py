from django.urls import path

from .views import *

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostRetrieveView.as_view(), name="post-detail"),
    path("profile/", UserUpdateView.as_view(), name="user-update"),
    path("favorite_presenters/", FavoritePresenterListView.as_view(), name="favorite-presenter-list"),
    path("favorite_shows/", FavoriteShowListView.as_view(), name="favorite-show-list"),
    path("choices/", ChoicesView.as_view(), name="choices"),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('ads-request/', AdvertisementRequest.as_view(), name='ads-request'),
]
