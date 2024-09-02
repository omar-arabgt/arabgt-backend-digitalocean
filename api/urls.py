from django.urls import path

from .views import *

urlpatterns = [
    path("home/", HomePageView.as_view(), name="home-page"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostRetrieveView.as_view(), name="post-detail"),
    path("post_action/<int:post_id>/", PostActionUpdateView.as_view(), name="post-action-update"),
    path("profile/", UserUpdateView.as_view(), name="user-update"),
    path('user/<int:pk>/delete', UserDeleteAPIView.as_view(), name='user_delete'),
    path("favorite_presenters/", FavoritePresenterListView.as_view(), name="favorite-presenter-list"),
    path("favorite_shows/", FavoriteShowListView.as_view(), name="favorite-show-list"),
    path("choices/", ChoicesView.as_view(), name="choices"),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('ads-request/', AdvertisementRequest.as_view(), name='ads-request'),
    path('subscribe_newsletter/', SubscribeNewsletter.as_view(), name='subscribe-newsletter'),
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:pk>/", QuestionRetrieveUpdateDestroyView.as_view(), name="question-retrieve-update-destroy"),
    path("pin_question/<question_id>/", PinQuestionView.as_view(), name="question-pin"),
    path("replies/", ReplyCreateView.as_view(), name="reply-create"),
    path("replies/<int:pk>/", ReplyRetrieveUpdateDestroyView.as_view(), name="reply-retrieve-update-destroy"),
    path("mobile_release/", MobileReleaseView.as_view(), name="mobile-release"),
    path('sections-posts/', SectionPostsView.as_view(), name='section-posts'),
    path('notifications/', NotificationList.as_view(), name='notifications'),
    path('forums/', ForumListView.as_view(), name='forums'),
    path('set_point/', SetPointView.as_view(), name='set-point'),
    path('verify_otp/', VerifyOTP.as_view(), name='verify_otp'),
]
