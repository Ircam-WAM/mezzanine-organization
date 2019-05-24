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
import json
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from organization.projects.models import *
from django.utils.text import slugify
from django.contrib.sites.models import Site
from copy import deepcopy


class Command(BaseCommand):
    help = """Retrieve content_fr of old mode Project
        from database Tue Feb 5 14:26:55 2019 +0100
    """

    def handle(self, *args, **options):

        json_path = '/srv/lib/mezzanine-organization/organization/projects/management/commands/projects.json'
        old_projects = self.read_json(json_path)

        project_pages = ProjectPage.objects.all()

        for project_page in project_pages:
            print(project_page.site_id)
            for old_project in old_projects:
                if old_project['pk'] == project_page.project_id:
                    # inject _fr in _en (because _fr became _en)
                    if not project_page.content_en:
                        project_page.content_en = project_page.content_fr
                    project_page.content_fr = old_project['fields']['content_fr']
                    project_page.save()

    def read_file(self, path):
        file = open(path, "r")
        data = file.read()
        file.close()
        return data

    def read_json(self, path):
        return json.loads(self.read_file(path))
