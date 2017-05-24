from django_auth_ldap.backend import LDAPBackend
from organization.network.models import Person
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class OrganizationLDAPBackend(LDAPBackend):

    def get_user(self, user_id):
        user = super().get_user(user_id)
        if user:
            try :
                person = Person.objects.get(email=user.email)
            except ObjectDoesNotExist:
                person = Person.objects.create(
                    title=user.first_name+" "+user.last_name,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                )
            if not person.user :
                person.user = user
                try :
                    person.save()
                except IntegrityError:
                    pass
        return user
