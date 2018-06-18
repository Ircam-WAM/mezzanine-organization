from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import Permission, User
import logging

logger = logging.getLogger()

@receiver(post_save, sender=User)
def set_default_permissions(sender, **kwargs):
    if kwargs['created']:  # Only for user creation
        u = kwargs['instance']
        if u and not u.has_perm('organization-projects.add_project'):
            p = Permission.objects.get(codename='add_project')
            if p:
                u.user_permissions.add(p)
                u.save()
                logger.info('Added permission "{0}" to user {1} (UID #{2})'.format(p.codename, u.username, u.id))
