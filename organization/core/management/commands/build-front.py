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

    def add_arguments(self, parser):

        parser.add_argument(
            '--force-npm',
            action='store_true',
            dest='force_npm',
            default=False,
            help='force npm install',
        )

        parser.add_argument(
            '--force-bower',
            action='store_true',
            dest='force_bower',
            default=False,
            help='force bower install',
        )

    def handle(self, *args, **options):
        self.force_npm = options['force_npm']
        self.force_bower = options['force_bower']
        themes_modules = []

        if not settings.HOST_THEMES:
            print('No settings.HOST_THEMES defined')
        else:
            print('Building front...')
            for host_theme in settings.HOST_THEMES:
                themes_module = host_theme[1]
                if not themes_module in themes_modules and themes_module in settings.INSTALLED_APPS:
                    themes_modules.append(themes_module)
            for theme in themes_modules:
                theme_path = apps.get_app_config(theme.split('.')[-1]).path
                os.chdir(theme_path)
                print('Building ' + theme)
                if not os.path.exists('node_modules') or self.force_npm:
                    subprocess.run(["npm", "install"])
                if not os.path.exists('static/vendors') or self.force_bower:
                    subprocess.run(["bower", "--allow-root", "install"])
                subprocess.run(["gulp", "build"])
