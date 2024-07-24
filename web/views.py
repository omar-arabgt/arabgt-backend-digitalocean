from django.contrib.auth import views as auth_views
from django.views.generic import ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import User, Newsletter
from django.http import HttpResponse
from django.db.models import Q
from .forms import *
import openpyxl
from django.utils.timezone import localtime


class UserListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of users with optional search functionality.

    Input:
    - Optional query parameter 'q' for searching users by username.

    Functionality:
    - Retrieves and lists users, optionally filtered by the search query.

    Output:
    - Renders the 'web/users/list.html' template with the user list and search context.
    """
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
    """
    Updates the details of a specific user.

    Input:
    - User ID in the URL and form data for updating the user.

    Functionality:
    - Retrieves the user by ID and updates their details using the provided form data.

    Output:
    - Renders the 'web/users/edit.html' template with the user data.
    - Redirects to the user list view upon successful update.
    """
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


def download_newsletter_excel(request):
    """
    Downloads an Excel file containing the newsletter subscriptions.

    Input:
    - No specific input required.

    Functionality:
    - Retrieves all newsletter subscriptions and writes them to an Excel file.

    Output:
    - Returns the Excel file as an HTTP response for download.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Newsletter"

    headers = ['ID', 'Email', 'Created At']
    ws.append(headers)

    newsletters = Newsletter.objects.all().values_list('id', 'email', 'created_at')
    for newsletter in newsletters:
        id, email, created_at = newsletter
        if created_at:
            created_at = localtime(created_at).replace(tzinfo=None)
        ws.append([id, email, created_at])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=newsletter.xlsx'

    wb.save(response)
    return response


class LoginView(auth_views.LoginView):
    """
    Handles user login.

    Input:
    - Form data containing username and password.

    Functionality:
    - Authenticates and logs in the user.

    Output:
    - Renders the 'web/login.html' template with the login form.
    """
    template_name = "web/login.html"
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تسجيل الدخول'
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Displays the home/dashboard page for logged-in users.

    Input:
    - No specific input required.

    Functionality:
    - Renders the home page for authenticated users.

    Output:
    - Renders the 'web/home.html' template.
    """
    template_name = "web/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'لوحة التحكم'
        return context
