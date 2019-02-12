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
from mezzanine.utils.sites import current_site_id

# from ulysses.competitions.models import Competition, CompetitionAttribute, CompetitionAttributeValue
from organization.projects.models import *


class Command(BaseCommand):
    """Copy ProjectContact geo data to ProjectResidency"""

    def handle(self, *args, **options):
        # project_call = ProjectCall.objects.get(id=options.get('project_call_id'))
        # competition = Competition.objects.get(id=options.get('competition_id'))

        for residency in ProjectResidency.objects.all():
            if not residency.mappable_location:
                contacts = residency.project.contacts.all()
                if contacts:
                    contact = contacts[0]
                    residency.address = contact.address
                    residency.postal_code = contact.postal_code
                    residency.city = contact.city
                    residency.country = contact.country
                    residency.save()
            else:
                residency.save()

