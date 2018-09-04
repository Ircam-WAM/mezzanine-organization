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

import requests
import datetime
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import *
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.apps import apps
from django.conf import settings


class Command(BaseCommand):
    
    help = "close implemented projects"

    def handle(self, *args, **options):
        today = datetime.datetime.today()
        projects = Project.objects.all()

        for project in projects:
            if project.call.date_to < today and project.residencies.all():
                project.validation_status = 5
                project.save()
            elif project.call.date_to < today and not project.residencies.all():
                project.validation_status = 6
                project.save()
