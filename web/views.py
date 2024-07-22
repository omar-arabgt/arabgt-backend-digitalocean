from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *


class LoginView(auth_views.LoginView):
    template_name = "web/login.html"
    form_class = CustomAuthenticationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "web/home.html"
