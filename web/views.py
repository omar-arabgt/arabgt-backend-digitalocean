from django.contrib.auth import views as auth_views
from django.views.generic import ListView, UpdateView, TemplateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import localtime
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils.timezone import localtime
import openpyxl

from api.models import User, Newsletter, DeletedUser, Group, Forum, Question, Reply
from api.tasks import send_push_notification, NOTIFICATION_ALL
from .utils import get_merged_user_data
from api.choices import COUNTRIES, GENDERS, STATUS, HOBBIES, INTERESTS, CAR_BRANDS, CAR_SORTING
from .forms import *

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'web/groups/list.html'
    context_object_name = 'groups'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        filters = Q()
        if query:
            filters &= Q(name__icontains=query)
        return Group.objects.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المجموعات'
        return context

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'web/groups/create.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'إنشاء مجموعة'
        return context

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'web/groups/edit.html'
    success_url = reverse_lazy('group_list')

    def get_object(self):
        return get_object_or_404(Group, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تعديل مجموعة'
        return context


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'web/users/list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        filters = Q(is_staff=False, is_superuser=False)
        if query:
            filters &= Q(username__icontains=query)

        return User.objects.filter(filters)

    def get_context_data(self, **kwargs):
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
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تفاصيل المستخدم'
        context['HOBBIES'] = HOBBIES
        context['INTERESTS'] = INTERESTS
        context['CAR_BRANDS'] = CAR_BRANDS
        context['CAR_SORTING'] = CAR_SORTING
        return context

class ForumListView(LoginRequiredMixin, ListView):
    model = Forum
    template_name = 'web/forums/list.html'
    context_object_name = 'forums'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        filters = Q()
        if query:
            filters &= Q(name__icontains=query)
        return Forum.objects.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المنتديات'
        return context

class ForumCreateView(LoginRequiredMixin, CreateView):
    model = Forum
    form_class = ForumForm
    template_name = 'web/forums/create.html'
    success_url = reverse_lazy('forum_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'انشاء منتدى'
        return context

class ForumUpdateView(LoginRequiredMixin, UpdateView):
    model = Forum
    form_class = ForumForm
    template_name = 'web/forums/edit.html'
    success_url = reverse_lazy('forum_list')

    def get_object(self):
        return get_object_or_404(Forum, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'تعديل منتدى'
        return context

class ExportUserListView(LoginRequiredMixin, ListView):
    template_name = 'web/export_users/list.html'
    context_object_name = 'merged_list'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality')
        country = self.request.GET.get('country')
        birthdate = self.request.GET.get('birthdate')
        gender = self.request.GET.get('gender')
        status = self.request.GET.get('status')

        return get_merged_user_data(query, nationality, country, birthdate, gender, status)

    def get_context_data(self, **kwargs):
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
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        nationality = self.request.GET.get('nationality')
        country = self.request.GET.get('country')
        birthdate = self.request.GET.get('birthdate')
        gender = self.request.GET.get('gender')
        status = self.request.GET.get('status')

        return get_merged_user_data(query, nationality, country, birthdate, gender, status)

    def get(self, request, *args, **kwargs):
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
        query = self.request.GET.get('q')
        if query:
            return Newsletter.objects.filter(Q(email__icontains=query))
        return Newsletter.objects.all()

    def get_context_data(self, **kwargs):
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
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        
        if user.is_superuser or user.is_staff:
            return redirect(self.success_url)

        user.delete()
        return redirect(self.success_url)

class DeletedUserListView(LoginRequiredMixin, ListView):
    model = DeletedUser
    template_name = 'web/deleted_users/list.html'
    context_object_name = 'deleted_user_list'
    paginate_by = 10

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'قائمة المستخدمين'
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

class TermsOfUsePrivacyPolicy(TemplateView):
    template_name = 'web/terms_of_us_privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_sidebar'] = True
        return context


class NotificationView(LoginRequiredMixin, TemplateView):
    """
    Displays the home/notifications page for logged-in users.

    Input:
    - No specific input required.

    Functionality:
    - Renders the notification page for authenticated users.

    Output:
    - Renders the 'web/notifications/container.html' template.
    """
    template_name = "web/notifications/container.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'إرسال التنبيهات'
        context['form'] = NotificationForm()

      
        notifications = Notification.objects.all().order_by('-created_at')
        paginator = Paginator(notifications, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context

    def post(self, request, *args, **kwargs):
        form = NotificationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            link = form.cleaned_data.get("link")
            send_push_notification.delay(NOTIFICATION_ALL, title, content, link)
            return redirect(reverse_lazy("send-notification"))
        return self.render_to_response(self.get_context_data(form=form))

class ForumGroupQuestionsView(LoginRequiredMixin, TemplateView):
    """
    Displays the home/questions page for logged-in users.

    Input:
    - No specific input required.

    Functionality:
    - Renders the questions for (group & fourms) page for authenticated users.

    Output:
    - Renders the 'web/questions.html' template.
    """

    template_name = "web/questions/questions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tab = self.request.GET.get('tab', 'forums')
        
        if tab == 'forums':
            questions = self.get_filtered_questions(tab)
            paginator = Paginator(questions, 10)
            page_number = self.request.GET.get('page')
            context['page_obj'] = paginator.get_page(page_number)
            context['forums_questions'] = context['page_obj']
        elif tab == 'groups':
            questions = self.get_filtered_questions(tab)
            paginator = Paginator(questions, 10)
            page_number = self.request.GET.get('page')
            context['page_obj'] = paginator.get_page(page_number)
            context['groups_questions'] = context['page_obj']

        context['active_tab'] = tab
        context[f'{tab}_search_query'] = self.request.GET.get('q', '')
        context[f'{tab}_question_id'] = self.request.GET.get('question_id', '')
        context[f'{tab}_group_filter'] = self.request.GET.get('forum_group', '')
        context[f'{tab}_date_filter'] = self.request.GET.get('date', '')
        context['forums'] = Forum.objects.all()
        context['groups'] = Group.objects.all()
        context['page_name'] = 'الأسئلة و النقاشات'

        return context

    def get_filtered_questions(self, tab):
        if tab == 'forums':
            questions = Question.objects.filter(forum__isnull=False)
            search_query = self.request.GET.get('q', '')
            question_id = self.request.GET.get('question_id', '')
            group_filter = self.request.GET.get('forum_group', '')
            date_filter = self.request.GET.get('date', '')

            if search_query:
                questions = questions.filter(
                    Q(user__username__icontains=search_query) | Q(user__id__icontains=search_query)
                )
            if question_id:
                questions = questions.filter(id=question_id)
            if group_filter:
                questions = questions.filter(forum__id=group_filter)
            if date_filter:
                questions = questions.filter(created_at__date=date_filter)

        elif tab == 'groups':
            questions = Question.objects.filter(group__isnull=False)
            search_query = self.request.GET.get('q', '')
            question_id = self.request.GET.get('question_id', '')
            group_filter = self.request.GET.get('forum_group', '')
            date_filter = self.request.GET.get('date', '')

            if search_query:
                questions = questions.filter(
                    Q(user__username__icontains=search_query) | Q(user__id__icontains=search_query)
                )
            if question_id:
                questions = questions.filter(id=question_id)
            if group_filter:
                questions = questions.filter(group__id=group_filter)
            if date_filter:
                questions = questions.filter(created_at__date=date_filter)

        return questions

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'web/questions/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        
        replies = question.replies.filter(parent_reply__isnull=True).annotate(
            total_likes=Count('reactions', filter=Q(reactions__reaction_type='like'))
        )
        
        context['replies'] = self.annotate_replies_with_likes(replies)
        context['no_sidebar'] = True
        context['page_name'] = 'تفاصيل السؤال'
        context['total_comments'] = count_replies(question)

        return context

    def annotate_replies_with_likes(self, replies):
        for reply in replies:
            reply.total_likes = reply.reactions.filter(reaction_type='like').count()
            if reply.replies.exists():
                reply.nested_replies = self.annotate_replies_with_likes(reply.replies.all())
        return replies

#  for getting nested reply count
def count_replies(question):
    total_replies = question.replies.count()
    for reply in question.replies.all():
        total_replies += count_nested_replies(reply)
    return total_replies

def count_nested_replies(reply):
    total_replies = reply.replies.count()
    for nested_reply in reply.replies.all():
        total_replies += count_nested_replies(nested_reply)
    return total_replies

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    question_id = reply.question.id if reply.question else reply.parent_reply.question.id

    if request.method == 'POST':
        reply.delete()
        return redirect(reverse('question_detail', args=[question_id]))

    return redirect(reverse('question_detail', args=[question_id]))

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question.delete()
        return redirect(reverse('question'))
    
    return redirect(reverse('question_detail', args=[question_id]))

