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

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = """Create a default admin user if it doesn't exist.
            you SHOULD change the password and the email afterwards!"""

    username = 'admin'
    password = 'admin'
    email = 'root@example.com'

    def handle(self, *args, **options):
        admin = User.objects.filter(username=self.username)
        if not admin:
            user = User(username=self.username)
            user.set_password(self.password)
            user.email = self.email
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print('User ' + self.username + ' created')
