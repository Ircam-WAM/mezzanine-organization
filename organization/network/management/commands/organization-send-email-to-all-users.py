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

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import time

class Command(BaseCommand):

    help = "send an email to all users"

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        subject = args[0] 
        html_email_path = args[1]

        subject = settings.EMAIL_SUBJECT_PREFIX + ' ' + subject
        sender = settings.DEFAULT_FROM_EMAIL

        f = open(html_email_path, 'r')
        html_message = f.read()
        f.close()

        emails = [ user.email for user in User.objects.filter(is_active=True) 
                if user.email and not 'example.com' in user.email ]
        #user_emails = ['pellerin@ircam.fr', 'pellerin@parisson.com']
        print(len(emails))

        chunk_size = 80
        chunks = [emails[x:x+chunk_size] for x in range(0, len(emails), chunk_size)]
        
        print(len(chunks))

        for chunk in chunks:
            print(len(chunk), chunk)
            message = EmailMessage(subject, html_message, sender, [], chunk,)
            message.content_subtype = 'html'
            message.send()
            time.sleep(10)
