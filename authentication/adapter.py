from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordResetForm
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        receiver = emailconfirmation.email_address.email

        context = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }

        subject = "Confirm your email"
        email_template = "email_confirmation_message.html"
        email_body = render_to_string(email_template, context)

        mail = EmailMessage(subject, email_body, to=[receiver])
        mail.content_subtype = "html"
        mail.send()

    def get_email_confirmation_redirect_url(self, request):
        return reverse("email_confirmed")


class CustomPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        user_model = get_user_model()
        users = user_model.objects.filter(is_active=True, email=email, emailaddress__verified=True)
        return users

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        reset_url = reverse("password_reset_confirm", args=[context["uid"], context["token"]])
        context["reset_url"] = build_absolute_uri(context["request"], reset_url)

        subject = "Reset Password"
        email_template = "password_reset_email.html"
        email_body = render_to_string(email_template, context)

        mail = EmailMessage(subject, email_body, to=[to_email])
        mail.content_subtype = "html"
        mail.send()
