from django_auth_ldap.backend import LDAPBackend
from organization.network.models import Person
from pprint import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class OrganizationLDAPBackend(LDAPBackend):

    def get_user(self, user_id):
        # a default created Person is assigned to the user
        user = super().get_user(user_id)
        if user:
            try :
                # get Person by mail
                person, created = Person.objects.get_or_create(email=user.email)

                # if the Person is the created default one
                if not user.person.first_name and not user.person.last_name:
                    old_person = user.person
                    # reassign the right Person
                    user.person = person
                    # delete the old one
                    old_person.delete()

                # if a Person is created, populate it
                if created:
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
