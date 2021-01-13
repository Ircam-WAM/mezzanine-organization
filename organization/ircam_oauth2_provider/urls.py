from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns,url
from .provider import IrcamAuthProvider
from django.conf import settings

try:
    if settings.OAUTH2_IRCAM == True:
        urlpatterns = default_urlpatterns(IrcamAuthProvider)
except AttributeError:
    urlpatterns = default_urlpatterns(IrcamAuthProvider)
