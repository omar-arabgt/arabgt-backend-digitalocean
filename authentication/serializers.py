from dj_rest_auth.serializers import PasswordResetSerializer, LoginSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer

from .adapter import CustomPasswordResetForm


class CustomFacebookLoginSerializer(SocialLoginSerializer):
    def post_signup(self, login, attrs):
        extra_data = login.account.extra_data
        user = login.account.user
        user.email = extra_data.get("id") + "@facebook.com"
        user.name = extra_data.get("name")
        user.save()


class CustomPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return CustomPasswordResetForm

    def get_email_options(self):
        extra_email_context = {
            "request": self.context.get("request")
        }
        return {"extra_email_context": extra_email_context}


class CustomLoginSerializer(LoginSerializer):

    def get_auth_user(self, username, email, password):
        return self.get_auth_user_using_allauth(username, email, password)
