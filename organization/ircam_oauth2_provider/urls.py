from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import IrcamAuthProvider

urlpatterns = default_urlpatterns(IrcamAuthProvider)
