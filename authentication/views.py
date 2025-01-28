from django.views.generic.base import TemplateView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView, Response

from .serializers import CustomSocialLoginSerializer, EmailChangeSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = CustomSocialLoginSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CustomSocialLoginSerializer


class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
    serializer_class = CustomSocialLoginSerializer


class EmailConfirmed(TemplateView):
    template_name = "authentication/email_confirmed.html"


class EmailChange(APIView):

    def post(self, request, *args, **kwargs):
        serializer = EmailChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        EmailAddress.objects.add_new_email(request, request.user, email)
        return Response("OK")
