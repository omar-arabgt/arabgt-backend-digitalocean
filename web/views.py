from django.contrib.auth import views as auth_views
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import User
from .forms import *

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'web/users/list.html'
    context_object_name = 'users'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'web/users/edit.html'
    success_url = reverse_lazy('user_list')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])


class LoginView(auth_views.LoginView):
    template_name = "web/login.html"
    form_class = CustomAuthenticationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "web/home.html"
