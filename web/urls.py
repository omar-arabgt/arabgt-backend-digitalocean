from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="web-login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("home/", HomeView.as_view(), name="home"),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('download_newsletter_excel/', download_newsletter_excel, name='download_newsletter_excel'),
]
