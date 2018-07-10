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

from datetime import datetime, timedelta
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

import mezzanine_agenda.models as ma_models
from mezzanine.generic.models import AssignedKeyword, Keyword

from organization.network.models import Department
from organization.agenda.models import EventDepartment 


class Command(BaseCommand):
    """Synchronize events from E-vement to mezzanine_agenda
    ex: python manage.py organization-agenda-move-events-from-site-to-site -f vertigo.starts.eu -t www.starts.eu -d Residencies
    """

    option_list = BaseCommand.option_list + (
        make_option('-f', '--from',
            dest='from_site_domain',
            help='define the domain of the source site'),
        make_option('-t', '--to',
            dest='to_site_domain',
            help='define the domain of the destination site'),
        make_option('-d', '--departement',
            dest='department',
            help='define the targeted department'),
    )

    def handle(self, *args, **kwargs):
        from_site = Site.objects.get(domain=kwargs.get('from_site_domain'))
        to_site = Site.objects.get(domain=kwargs.get('to_site_domain'))
        department = Department.objects.get(name=kwargs.get('department'))

        events = ma_models.Event.objects.filter(site=from_site)
        print(events)
        for event in events:
            event.site = to_site
            event.save()
            event_department = EventDepartment(event=event, department=department)
            event_department.save()


