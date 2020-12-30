import requests
from allauth.socialaccount.models import (SocialAccount,SocialLogin)
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import IrcamAuthProvider
from django.conf import settings
from django.contrib.auth.models import User
from organization.network.models import Person
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

import logging

class IrcamAuthAdapter(OAuth2Adapter):

    if not hasattr(settings, 'OAUTH_SERVER_BASEURL'):
        raise Exception("Couldn't find OAUTH_SERVER_BASEURL in the settings")
    
    logger = logging.getLogger('ircamauth')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG) if settings.DEBUG else logger.setLevel(logging.INFO)
   
    provider_id = IrcamAuthProvider.id
    access_token_url = '{}/o/token/'.format(settings.OAUTH_SERVER_BASEURL)  # Called programmatically, must be reachable from container
    authorize_url = '{}/o/authorize/'.format(settings.USER_SERVER_BASEURL)  # Accessed by the client so must be host-reachable
    profile_url = '{}/profile/'.format(settings.OAUTH_SERVER_BASEURL)

    def create_or_update_person(self,user):
        try :
            person, created = Person.objects.get_or_create(user_id=user.id)            
            person.user = user
            person.title = user.first_name+" "+user.last_name
            person.first_name = user.first_name
            person.last_name = user.last_name
            person.email = user.email

            person.save()

        except ObjectDoesNotExist:
            person = Person.objects.get(
                user_id=user.id
            )
        except IntegrityError:
            pass

    def create_user_socialaccount(self,request,extra_data):

        user, created = User.objects.update_or_create(
            username = extra_data['username'],
            defaults={
                'first_name': extra_data['first_name'],
                'last_name': extra_data['last_name'],
                'is_active': True,
                'is_superuser': False,
                'is_staff': False,
                'email': extra_data['email'],
            }
        )
        user.save()
        self.logger.info('Local user {0} id:{1} username:{2} email:{3}'.format('created: ' if created else 'updated: ',user.id,user.username,user.email))
        
        # Creating or updating Person
        self.create_or_update_person(user)
       
        # Creating the allauth social account so the user can log in through Ircam Auth
        social_account = SocialAccount(user=user,
                                    provider='ircamauth',
                                    uid=extra_data['id'],
                                    extra_data={'id': user.id, 'username': user.username, 'email': user.email})
        social_account.save()
        self.logger.info('Social account created. User {0} '.format(user.username))
        return self.get_provider().sociallogin_from_response(request, extra_data)

    def update_localuser(self,social_user,extra_data):
        from django.contrib.auth.models import User

        user = User.objects.filter( username__contains=extra_data['username'] )[0]
        if (  
                user.email != extra_data['email'] or 
                user.first_name != extra_data['first_name'] or 
                user.last_name != extra_data['last_name'] 
            ) :
            user.username = extra_data['username']
            user.email = extra_data['email']
            user.first_name = extra_data['first_name']
            user.last_name = extra_data['last_name']
            user.is_active = True
            user.save()
            self.logger.info('User {0} updated, email:{1}, firstN:{2}, LastN:{3}'
                .format(user.username,user.email,user.first_name,user.last_name))
            # Creating or updating Person
            self.create_or_update_person(user)
 
    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()

        self.logger.debug("EXTRA_DATA:")
        self.logger.debug(str(extra_data))
        try:
            social_user = self.get_provider().sociallogin_from_response(request, extra_data)
            saccount = SocialAccount.objects.get(
                provider=social_user.account.provider, uid=social_user.account.uid
            )
            self.update_localuser(social_user,extra_data)
        except:
            social_user = self.create_user_socialaccount(request,extra_data)

        self.logger.info('User logged in: {0} '.format(social_user.user.username))        
        return social_user


oauth2_login = OAuth2LoginView.adapter_view(IrcamAuthAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(IrcamAuthAdapter)
