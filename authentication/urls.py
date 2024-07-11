from django.urls import path, include
from allauth.account.views import ConfirmEmailView

from .views import *


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('register/account-confirm-email/<key>/', ConfirmEmailView.as_view(template_name="confirm_email.html"), name='account_confirm_email'),
    path('register/', include('dj_rest_auth.registration.urls')),
    path('email_confirmed/', EmailConfirmed.as_view(), name='email_confirmed'),
    path('apple/', AppleLogin.as_view(), name='apple_login'),
    path('facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
