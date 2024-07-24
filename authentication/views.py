from django.views.generic.base import TemplateView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import CustomFacebookLoginSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = CustomFacebookLoginSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter


class EmailConfirmed(TemplateView):
    template_name = "authentication/email_confirmed.html"
