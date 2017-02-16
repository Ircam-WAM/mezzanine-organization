# -*- coding: utf-8 -*-

from imaplib import IMAP4_SSL
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from guardian.backends import ObjectPermissionBackend  # used to ad has_perm to IMAPBackend


class IMAPBackend(ObjectPermissionBackend):
    # Create an authentication method
    # This is called by the standard Django login procedure

    # ! authentificated user with this system will not be able to
    # login user admin, they are not keystaff
    def authenticate(self, username=None, password=None):
        try:
            # Check if this user is valid on the mail server
            c = IMAP4_SSL('imap.ircam.fr')
            c.login(username, password)
            c.logout()
        except:
            return None

        try:
            # Check if the user exists in Django's local database
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a user in Django's local database
            user = User.objects.create_user(username, '%s@ircam.fr' % (username), 'passworddoesntmatter')
            user.save()
            send_mail('NEW USER', '%s' % (user.username), settings.DEFAULT_FROM_EMAIL, [admin[1] for admin in settings.ADMINS], fail_silently=True)
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
