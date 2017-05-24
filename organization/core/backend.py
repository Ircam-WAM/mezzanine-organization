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
                person = Person.objects.get(user=user)
                person.title=user.first_name+" "+user.last_name
                person.first_name=user.first_name
                person.last_name=user.last_name
                person.email=user.email
                try :
                    person.save()
                except IntegrityError:
                    pass
            except ObjectDoesNotExist:
                person = Person.objects.get(
                    email=user.email
                )
        return user
