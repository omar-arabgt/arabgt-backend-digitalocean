from django.urls import path

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="web-login"),
    path("home/", HomeView.as_view(), name="home"),
]