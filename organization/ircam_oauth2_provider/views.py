import requests
from allauth.socialaccount.models import (SocialAccount,SocialLogin)
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import IrcamAuthProvider
from django.conf import settings
from django.contrib.auth.models import User
from organization.network.models import Person
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import logout
from django.shortcuts import redirect
from .utils import createOrUpdateLocalEntities
from rest_framework.response import Response

import logging

logger = logging.getLogger('ircamauth')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG) if settings.DEBUG else logger.setLevel(logging.WARNING)
 
class IrcamAuthAdapter(OAuth2Adapter):

    if not hasattr(settings, 'OAUTH_SERVER_BASEURL'):
        raise Exception("Couldn't find OAUTH_SERVER_BASEURL in the settings")
    
    logger.setLevel(logging.DEBUG) if settings.DEBUG else logger.setLevel(logging.WARNING)
   
    provider_id = IrcamAuthProvider.id
    access_token_url = '{}/o/token/'.format(settings.OAUTH_SERVER_BASEURL)  # Called programmatically, must be reachable from container
    authorize_url = '{}/o/authorize/'.format(settings.USER_SERVER_BASEURL)  # Accessed by the client so must be host-reachable
    profile_url = '{}/profile/'.format(settings.OAUTH_SERVER_BASEURL)

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        logger.info("complete_login. extra_data:{0}".format(extra_data))
        if createOrUpdateLocalEntities(extra_data):
            social_login = self.get_provider().sociallogin_from_response(request, extra_data)
        else :
            logger.error("Failed to create user and socialAccount with extra_data: {0}".format(extra_data))
            return None

        return social_login


def serverLogout(request):
    if not request.user.is_authenticated:
        pass
    else :
        logout(request)
    return redirect("/")

oauth2_login = OAuth2LoginView.adapter_view(IrcamAuthAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(IrcamAuthAdapter)
