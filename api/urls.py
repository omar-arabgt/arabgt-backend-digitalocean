from django.urls import path

from .views import *

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home-page"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostRetrieveView.as_view(), name="post-detail"),
    path("saved_posts/", SavedPostListCreateView.as_view(), name="saved-post-list-create"),
    path("saved_posts/<int:pk>/", SavedPostUpdateView.as_view(), name="saved-post-update"),
    path("profile/", UserUpdateView.as_view(), name="user-update"),
    path('user/<int:pk>/delete', UserDeleteAPIView.as_view(), name='user_delete'),
    path("favorite_presenters/", FavoritePresenterListView.as_view(), name="favorite-presenter-list"),
    path("favorite_shows/", FavoriteShowListView.as_view(), name="favorite-show-list"),
    path("choices/", ChoicesView.as_view(), name="choices"),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('ads-request/', AdvertisementRequest.as_view(), name='ads-request'),
    path('subscribe_newsletter', SubscribeNewsletter.as_view(), name='subscribe-newsletter'),
    path('unsubscribe_newsletter', UnsubscribeNewsletter.as_view(), name='unsubscribe-newsletter'),
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:pk>/", QuestionRetrieveUpdateDestroyView.as_view(), name="question-retrieve-update-destroy"),
]
