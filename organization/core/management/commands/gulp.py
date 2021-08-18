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

import os
import subprocess
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Apply gulp command in current theme"

    def handle(self, *args, **options):
        themes_modules = []

        if not settings.HOST_THEMES:
            print('No settings.HOST_THEMES defined')
        else:
            for host_theme in settings.HOST_THEMES:
                themes_module = host_theme[1]
                if themes_module not in themes_modules and\
                        themes_module in settings.INSTALLED_APPS:
                    themes_modules.append(themes_module)
            for theme in themes_modules:
                theme_path = apps.get_app_config(theme.split('.')[-1]).path
                os.chdir(theme_path)
                print('Building ' + theme)
                subprocess.run(["gulp"])
