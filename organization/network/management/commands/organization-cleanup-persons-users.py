# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import uuid
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from organization.network.models import Person


class Command(BaseCommand):
    help = "Create a user for every Person"

    def handle(self, *args, **options):
        persons = Person.objects.filter(user=None)

        person_emails = []
        for person in persons:
            if not person.email in person_emails:
                person_emails.append(person.email)

        for email in person_emails:
            persons = Person.object.filter(email=email)
            persons_bio = persons.exclude(bio__isnull=False)
            if persons:
                if persons.count() != persons_bio.count():
                    person = persons_bio[0]
                else persons:
                    person = persons[0]

                users = User.objects.filter(email=email)
                if users:
                    user = users[0]
                else:
                    user = User(email=email)
                    user.username = uuid.uuid4()
                    user.save()
                    user.username = 'user-' + str(user.id)
                    user.save()

                person.user = user
                person.save()

                for p in persons:
                    if p != person:
                        p.delete()



