from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import IrcamAuthProvider

from django.conf import settings

if settings.OAUTH2_IRCAM:
    urlpatterns = default_urlpatterns(IrcamAuthProvider)
