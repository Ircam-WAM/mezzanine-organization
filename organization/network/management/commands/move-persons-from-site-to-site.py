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
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.network.models import Person
from organization.network.api import *
from django.utils.text import slugify
from django.contrib.sites.models import Site
import datetime

class Command(BaseCommand):
    help = """Move Person from one site to another regarding the year of the creation date
    """

    target_site_id = 4
    year = 2021

    def handle(self, *args, **options):
        persons = Person.objects.all()
        site = Site.objects.get(id=self.target_site_id)

        for person in persons:
            if person.created.year == self.year:
                person.site = site
                person.save()
