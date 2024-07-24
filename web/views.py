from django.contrib.auth import views as auth_views
from django.views.generic import ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import User
from django.db.models import Q
from .forms import *

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'web/users/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(Q(username__icontains=query))
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المستخدمين'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'web/users/edit.html'
    success_url = reverse_lazy('user_list')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تعديل المستخدم'
        return context

class LoginView(auth_views.LoginView):
    template_name = "web/login.html"
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تسجيل الدخول'
        return context

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "web/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'لوحة التحكم'
        return context
