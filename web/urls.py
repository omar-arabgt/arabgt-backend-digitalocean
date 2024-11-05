from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="web-login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path("home/", HomeView.as_view(), name="home"),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/view/', ViewUserView.as_view(), name='user_view'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('deleted_user/', DeletedUserListView.as_view(), name='deleted_user_list'),
    path('export_users/', ExportUserListView.as_view(), name='export_user_list'),
    path('export_users_excel/', ExportUserToExcelView.as_view(), name='export_users_excel'),

    path('forums/', ForumListView.as_view(), name='forum_list'),
    path('forums/create', ForumCreateView.as_view(), name='forum_create'),
    path('forums/<int:pk>/edit/', ForumUpdateView.as_view(), name='forum_edit'),

    path('notifications/', NotificationView.as_view(), name='notifications'),
    
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),

    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('download_newsletter_excel/', download_newsletter_excel, name='download_newsletter_excel'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('term-of-use-privacy-policy/', TermsOfUsePrivacyPolicy.as_view(), name='term_of_use_privacy_policy'),
    path('notification/', NotificationView.as_view(), name='send-notification'),
    
    path('questions/', ForumGroupQuestionsView.as_view(), name='questions'),
    path('questions/<int:pk>/view', QuestionDetailView.as_view(), name='question_detail'),

    path('delete/reply/<int:reply_id>/', delete_reply, name='delete_reply'),
    path('delete/question/<int:question_id>/', delete_question, name='delete_question'),
]
