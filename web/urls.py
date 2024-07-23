from django.urls import path

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="web-login"),
    path("home/", HomeView.as_view(), name="home"),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
]
