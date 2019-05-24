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
from organization.projects.models import *
from django.utils.text import slugify
from django.contrib.sites.models import Site
from copy import deepcopy


class Command(BaseCommand):
    help = """Copy project pages from on site to another
    """

    def add_arguments(self, parser):

        parser.add_argument('-f',
            '--from-site-id',
            dest='from_site_id',
            help='from site id'
        )

        parser.add_argument('-t',
        '--to-site-id',
            dest='to_site_id',
            help='to site id'
        )

    def handle(self, *args, **options):
        from_site_id = int(options.get('from_site_id'))
        to_site_id = int(options.get('to_site_id'))

        from_site = Site.objects.get(id=from_site_id)
        to_site = Site.objects.get(id=to_site_id)

        for project_page in ProjectPage.objects.filter(site=from_site):

            to_project_page = deepcopy(project_page)
            to_project_page.pk = None
            to_project_page.site = to_site
            to_project_page.save()

            for project_page_block in project_page.blocks.all():
                to_project_page_block = ProjectPageBlock()
                for field in project_page_block._meta.fields:
                    setattr(to_project_page_block, field.name, getattr(project_page_block, field.name))
                to_project_page_block.project_page = to_project_page
                to_project_page_block.save()

            for project_page_image in project_page.images.all():
                to_project_page_image = ProjectPageImage()
                for field in project_page_image._meta.fields:
                    setattr(to_project_page_image, field.name, getattr(project_page_image, field.name))
                to_project_page_image.project_page = to_project_page
                to_project_page_image.save()

            for dynamic_content_project in project_page.dynamic_content_project_pages.all():
                to_project_page_dynamic_content = DynamicContentProjectPage()
                for field in dynamic_content_project._meta.fields:
                    setattr(to_project_page_dynamic_content, field.name, getattr(dynamic_content_project, field.name))
                to_project_page_dynamic_content.project_page = to_project_page
                to_project_page_dynamic_content.save()