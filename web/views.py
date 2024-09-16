from django.contrib.auth import views as auth_views
from django.views.generic import ListView, UpdateView, TemplateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import localtime
import openpyxl

from api.models import User, Newsletter, DeletedUser, Group, Forum
from api.tasks import send_push_notification, NOTIFICATION_ALL
from .utils import get_merged_user_data
from api.choices import COUNTRIES, GENDERS, STATUS, HOBBIES, INTERESTS, CAR_BRANDS, CAR_SORTING
from .forms import *

class GroupListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of groups with optional search functionality.

    Input:
    - Optional query parameter 'q' for searching groups by name.

    Functionality:
    - Retrieves and lists groups, optionally filtered by the search query.

    Output:
    - Renders the 'web/groups/list.html' template with the group list and search context.
    """
    model = Group
    template_name = 'web/groups/list.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        """
        Filters the list of groups based on the search query.
        """
        query = self.request.GET.get('q', '')
        filters = Q()
        if query:
            filters &= Q(name__icontains=query)
        return Group.objects.filter(filters)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المجموعات'
        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new group.

    Input:
    - Form data containing group details.

    Functionality:
    - Creates a new group using the submitted data.

    Output:
    - Redirects to the group list view upon successful creation.
    """
    model = Group
    form_class = GroupForm
    template_name = 'web/groups/create.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'إنشاء مجموعة'
        return context


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows authenticated users to update an existing group.

    Input:
    - Form data containing updated group details.

    Functionality:
    - Updates the specified group with the new data.

    Output:
    - Redirects to the group list view upon successful update.
    """
    model = Group
    form_class = GroupForm
    template_name = 'web/groups/edit.html'
    success_url = reverse_lazy('group_list')

    def get_object(self):
        """
        Retrieves the group object to be updated.
        """
        return get_object_or_404(Group, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تعديل مجموعة'
        return context


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
        """
        Filters the list of users based on the search query and excludes staff and superusers.
        """
        query = self.request.GET.get('q', '')
        filters = Q(is_staff=False, is_superuser=False)
        if query:
            filters &= Q(username__icontains=query)

        return User.objects.filter(filters)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المستخدمين'
        return context


class ViewUserView(LoginRequiredMixin, DetailView):
    """
    Displays the details of a specific user.

    Input:
    - User ID in the URL to retrieve and display user data.

    Functionality:
    - Retrieves the user by ID and displays their details.

    Output:
    - Renders the 'web/users/view.html' template with the user data.
    """
    model = User
    template_name = 'web/users/view.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """
        Adds additional context data such as hobbies, interests, car brands, and sorting options.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تفاصيل المستخدم'
        context['HOBBIES'] = HOBBIES
        context['INTERESTS'] = INTERESTS
        context['CAR_BRANDS'] = CAR_BRANDS
        context['CAR_SORTING'] = CAR_SORTING
        return context


class ForumListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of forums with optional search functionality.

    Input:
    - Optional query parameter 'q' for searching forums by name.

    Functionality:
    - Retrieves and lists forums, optionally filtered by the search query.

    Output:
    - Renders the 'web/forums/list.html' template with the forum list and search context.
    """
    model = Forum
    template_name = 'web/forums/list.html'
    context_object_name = 'forums'
    paginate_by = 10

    def get_queryset(self):
        """
        Filters the list of forums based on the search query.
        """
        query = self.request.GET.get('q', '')
        filters = Q()
        if query:
            filters &= Q(name__icontains=query)
        return Forum.objects.filter(filters)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المنتديات'
        return context


class ForumCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new forum.

    Input:
    - Form data containing forum details.

    Functionality:
    - Creates a new forum using the submitted data.

    Output:
    - Redirects to the forum list view upon successful creation.
    """
    model = Forum
    form_class = ForumForm
    template_name = 'web/forums/create.html'
    success_url = reverse_lazy('forum_list')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'انشاء منتدى'
        return context


class ForumUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows authenticated users to update an existing forum.

    Input:
    - Form data containing updated forum details.

    Functionality:
    - Updates the specified forum with the new data.

    Output:
    - Redirects to the forum list view upon successful update.
    """
    model = Forum
    form_class = ForumForm
    template_name = 'web/forums/edit.html'
    success_url = reverse_lazy('forum_list')

    def get_object(self):
        """
        Retrieves the forum object to be updated.
        """
        return get_object_or_404(Forum, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تعديل منتدى'
        return context


class ExportUserListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated and filtered list of merged User and DeletedUser data.

    Input:
    - Optional query parameters for filtering the user list by various attributes such as nationality, country, birthdate, etc.

    Functionality:
    - Retrieves and lists merged User and DeletedUser data, optionally filtered by the provided query parameters.

    Output:
    - Renders the 'web/export_users/list.html' template with the merged user list and filtering options.
    """
    template_name = 'web/export_users/list.html'
    context_object_name = 'merged_list'
    paginate_by = 10

    def get_queryset(self):
        """
        Retrieves and filters the merged user data based on the query parameters.
        """
        query = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality')
        country = self.request.GET.get('country')
        birthdate = self.request.GET.get('birthdate')
        gender = self.request.GET.get('gender')
        status = self.request.GET.get('status')

        return get_merged_user_data(query, nationality, country, birthdate, gender, status)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as filter options and the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Merged User and DeletedUser List'
        context['search_query'] = self.request.GET.get('q', '')
        context['nationality_filter'] = self.request.GET.get('nationality', '')
        context['country_filter'] = self.request.GET.get('country', '')
        context['birthdate_filter'] = self.request.GET.get('birthdate', '')
        context['gender_filter'] = self.request.GET.get('gender', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['GENDERS'] = GENDERS
        context['STATUS'] = STATUS
        context['COUNTRIES'] = COUNTRIES
        return context


class ExportUserToExcelView(LoginRequiredMixin, ListView):
    """
    Exports the filtered merged User and DeletedUser data to an Excel file.

    Input:
    - Optional query parameters for filtering the user data by various attributes such as nationality, country, birthdate, etc.

    Functionality:
    - Retrieves and filters the merged user data, writes it to an Excel file, and returns the file as an HTTP response.

    Output:
    - Returns the Excel file containing the merged user data for download.
    """

    def get_queryset(self):
        """
        Retrieves and filters the merged user data based on the query parameters.
        """
        query = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality')
        country = self.request.GET.get('country')
        birthdate = self.request.GET.get('birthdate')
        gender = self.request.GET.get('gender')
        status = self.request.GET.get('status')

        return get_merged_user_data(query, nationality, country, birthdate, gender, status)

    def get(self, request, *args, **kwargs):
        """
        Generates and returns an Excel file containing the filtered user data.
        """
        queryset = self.get_queryset()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Users and Deleted Users"

        headers = [
            'ID', # رقم المستخدم
            'Status', # الحالة
            'First Name', # اسم الاول
            'Last Name', # الاسم الاخير
            'Nick Name', # الكنية
            'Birth Date', # تاريخ الميلاد
            'Gender', # الجنسية
            'Nationality', # دولة الإقامة
            'Country', # الجنس
            'Rank', # فئة
        ]

        ws.append(headers)

        for user in queryset:
            ws.append([
                user['id'],
                "محذوف" if user['status'] == "deleted" else "مفعل",
                user['first_name'],
                user['last_name'],
                user['nick_name'],
                user['birth_date'],
                "ذكر" if user['gender'] == "M" else "انثي",
                user['get_nationality_display'],
                user['get_country_display'],
                ""
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=exported_users.xlsx'
        wb.save(response)
        return response


class NewsletterListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of newsletter subscriptions with optional search functionality.

    Input:
    - Optional query parameter 'q' for searching newsletter subscriptions by email.

    Functionality:
    - Retrieves and lists newsletter subscriptions, optionally filtered by the search query.

    Output:
    - Renders the 'web/newsletter/list.html' template with the newsletter list and search context.
    """
    model = Newsletter
    template_name = 'web/newsletter/list.html'
    context_object_name = 'newsletter_list'
    paginate_by = 10

    def get_queryset(self):
        """
        Filters the newsletter list based on the search query.
        """
        query = self.request.GET.get('q')
        if query:
            return Newsletter.objects.filter(Q(email__icontains=query))
        return Newsletter.objects.all()

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name and search query.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة النشرة البريدية'
        context['search_query'] = self.request.GET.get('q', '')
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a specific user's information.

    Input:
    - User ID is passed in the URL.

    Functionality:
    - Retrieves the user by ID and deletes their information.

    Output:
    - Redirects to the user list view upon successful deletion.
    """
    model = User
    success_url = reverse_lazy('user_list')
    
    def get_object(self, queryset=None):
        """
        Retrieves the user object to be deleted.
        """
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """
        Handles the deletion of the user, ensuring that superusers and staff members cannot be deleted.
        """
        user = self.get_object()
        
        if user.is_superuser or user.is_staff:
            return redirect(self.success_url)

        user.delete()
        return redirect(self.success_url)


class DeletedUserListView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of deleted users with optional search and filter functionality.

    Input:
    - Optional query parameters for searching and filtering deleted users by various attributes such as username, nationality, country, birthdate, etc.

    Functionality:
    - Retrieves and lists deleted users, optionally filtered by the search and filter criteria.

    Output:
    - Renders the 'web/deleted_users/list.html' template with the deleted user list and filter options.
    """
    model = DeletedUser
    template_name = 'web/deleted_users/list.html'
    context_object_name = 'deleted_user_list'
    paginate_by = 10

    def get_queryset(self):
        """
        Filters the list of deleted users based on the search and filter criteria.
        """
        query = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality')
        country = self.request.GET.get('country')
        birthdate = self.request.GET.get('birthdate')

        filters = Q()

        if query:
            filters &= Q(username__icontains=query)
        if nationality:
            filters &= Q(nationality=nationality)
        if country:
            filters &= Q(country=country)
        if birthdate:
            try:
                date = parse_date(birthdate)
                if date:
                    filters &= Q(birth_date__gt=date)
            except ValueError:
                pass

        return DeletedUser.objects.filter(filters)

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as filter options and the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المستخدمين المحذوفين'
        context['search_query'] = self.request.GET.get('q', '')
        context['nationality_filter'] = self.request.GET.get('nationality', '')
        context['country_filter'] = self.request.GET.get('country', '')
        context['birthdate_filter'] = self.request.GET.get('birthdate', '')
        context['car_brand_filter'] = self.request.GET.get('car_brand', '')
        context['COUNTRIES'] = COUNTRIES
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
        """
        Adds additional context data, such as the page name.
        """
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
        """
        Adds additional context data, such as the page name.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'لوحة التحكم'
        return context


class TermsOfUsePrivacyPolicy(TemplateView):
    """
    Displays the Terms of Use and Privacy Policy page.

    Input:
    - No specific input required.

    Functionality:
    - Renders the Terms of Use and Privacy Policy page.

    Output:
    - Renders the 'web/terms_of_us_privacy_policy.html' template.
    """
    template_name = 'web/terms_of_us_privacy_policy.html'

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as a flag to hide the sidebar.
        """
        context = super().get_context_data(**kwargs)
        context['no_sidebar'] = True
        return context


class NotificationView(LoginRequiredMixin, TemplateView):
    """
    Displays the notifications page for logged-in users and allows sending notifications.

    Input:
    - Form data containing notification details such as title, content, and link.

    Functionality:
    - Renders the notifications page with the form to send new notifications.
    - Lists all sent notifications with pagination.

    Output:
    - Renders the 'web/notifications/container.html' template with the notification form and list of sent notifications.
    """
    template_name = "web/notifications/container.html"
    paginate_by = 10  # Number of notifications per page

    def get_context_data(self, **kwargs):
        """
        Adds additional context data, such as the page name, form, and paginated notifications.
        """
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'إرسال التنبيهات'
        context['form'] = NotificationForm()

        # Fetching sent notifications with pagination
        notifications = Notification.objects.all().order_by('-created_at')
        paginator = Paginator(notifications, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the submission of the notification form and sends notifications to all users.
        """
        form = NotificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            link = form.cleaned_data.get("link")
            send_push_notification.delay(NOTIFICATION_ALL, title, content, link)
            return redirect(reverse_lazy("send-notification"))
        return self.render_to_response(self.get_context_data(form=form))
