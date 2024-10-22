from django.utils.translation import gettext as _
from rest_framework.serializers import ValidationError
from dj_rest_auth.serializers import PasswordResetSerializer, LoginSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer

from .adapter import CustomPasswordResetForm


class CustomSocialLoginSerializer(SocialLoginSerializer):

    def post_signup(self, login, attrs):
        if login.account.provider == "facebook":
            extra_data = login.account.extra_data
            user = login.account.user
            user.email = extra_data.get("id") + "@facebook.com"
            user.name = extra_data.get("name")
            user.save()

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except Exception as e:
            if str(e) == "account/email/account_already_exists_subject.txt":
                #  library throws this error when there is already registered user by another social provider.
                #  Ex: user login with google first, then try with google or apple.
                raise ValidationError(_("This account is already exists"))
            raise e


class CustomPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return CustomPasswordResetForm

    def get_email_options(self):
        self.reset_form._request = self.context.get("request")
        extra_email_context = {
            "request": self.context.get("request")
        }
        return {"extra_email_context": extra_email_context}


class CustomLoginSerializer(LoginSerializer):

    def get_auth_user(self, username, email, password):
        return self.get_auth_user_using_allauth(username, email, password)
