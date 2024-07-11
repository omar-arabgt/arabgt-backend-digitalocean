from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from allauth.account.adapter import DefaultAccountAdapter



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
