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

import os, time
import subprocess
from django.apps import apps
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections

class Command(BaseCommand):
    help = "Build the front with bower and gulp"

    def handle(self, *args, **options):
        for ht in settings.HOST_THEMES:
            # search for theme name in INSTALLED_APPS
            # to get the ones that are used
            if ht[1] in settings.INSTALLED_APPS:
                theme = ht[1]
                if theme :
                    theme_path = apps.get_app_config(theme.split('.')[-1]).path
                    os.chdir(theme_path)
                    subprocess.run(["bower", "--allow-root", "install"])
                    subprocess.run(["gulp", "build"])
