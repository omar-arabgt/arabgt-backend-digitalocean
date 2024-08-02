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
    
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),

    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('download_newsletter_excel/', download_newsletter_excel, name='download_newsletter_excel'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='privacy_policy'),
    path('terms-of-usage/', TermsOfUsage.as_view(), name='terms_of_usage'),
]
