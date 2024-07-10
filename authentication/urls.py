from django.urls import path, include
import dj_rest_auth

from .views import *


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('register/', include('dj_rest_auth.registration.urls')),
    path('apple/', AppleLogin.as_view(), name='apple_login'),
    path('facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
