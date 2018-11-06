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

from ulysses.competitions.models import Competition, CompetitionAttribute, CompetitionAttributeValue
from organization.projects.models import ProjectCall


class Command(BaseCommand):
    """
    """

    option_list = BaseCommand.option_list = (
        make_option('-p', '--project_call_id',
            dest='project_call_id',
            help='define the source call id'),
        make_option('-c', '--competition',
            dest='competition_id',
            help='define the destination competition id'),
    )

    competition_attribute_key = 'techprojectchoice'

    def handle(self, *args, **options):
        # project_call = ProjectCall.objects.get(id=options.get('project_call_id'))
        # competition = Competition.objects.get(id=options.get('competition_id'))
        project_call = ProjectCall.objects.get(id=14)
        competition = Competition.objects.get(id=1)
        competition_attribute = CompetitionAttribute.objects.get(competition=competition, key=self.competition_attribute_key)
        attributes = competition_attribute.competitionattributevalue_set.all()
        attribute_keys = [attribute.key for attribute in attributes if attribute.value]
        print(attribute_keys)

        for project in project_call.projects.filter(validation_status=3):
            if not project.slug[:99] in attribute_keys:
                # print(competition_attribute, project.slug, project.title)
                CompetitionAttributeValue.objects.create(attribute=competition_attribute, key=project.slug[:99], acronym=project.title[:24], value=project.title[:99])

