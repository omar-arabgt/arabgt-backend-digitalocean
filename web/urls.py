from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="web-login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("home/", HomeView.as_view(), name="home"),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('deleted_user/', DeletedUserListView.as_view(), name='deleted_user_list'),
    path('export_users/', ExportUserListView.as_view(), name='export_user_list'),
    path('export_users_excel/', ExportUserToExcelView.as_view(), name='export_users_excel'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('news/', download_newsletter_excel, name='download_newsletter_excel'),
    path('download_newsletter_excel/', download_newsletter_excel, name='download_newsletter_excel'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),

    path('forums/', ForumListView.as_view(), name='forum_list'),
    path('forums/create', ForumCreateView.as_view(), name='forum_create'),
    path('forums/<int:pk>/delete/', ForumUpdateView.as_view(), name='forum_edit'),
]
