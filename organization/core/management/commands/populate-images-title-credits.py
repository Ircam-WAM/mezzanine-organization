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
import re

from datetime import datetime, timedelta
from optparse import make_option
from django.apps import apps

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from organization.core.models import Image

class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in Image.__subclasses__():
            print("model", model)
            # objs = model.objects.all()
            # for obj in objs:
            #     obj.title_en = obj.title
            #     obj.credits_en = obj.credits
            #     obj.save()
