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

from organization.projects.models import Project,Repository,RepositorySystem,ProjectResidency,ProjectResidencyEvent
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from organization.agenda.models import Event,EventLocation
from mezzanine.utils.tests import TestCase
from django.utils.translation import ugettext_lazy as _
import datetime

PROJECT_STATUS_CHOICES = (
    (0, _('rejected')),
    (1, _('pending')),
    (2, _('in process')),
    (3, _('accepted')),
)

class ProjectTests(TestCase):

    def setUp(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        super(ProjectTests, self).setUp()
                
        self.project_test = Project.objects.create(title='test project')
        self.current_project = Project.objects.create(title='current project',date_from = yesterday, date_to = tomorrow)
        self.past_project = Project.objects.create(title='past project',date_from = yesterday, date_to = yesterday)
        self.futur_project = Project.objects.create(title='futur project',date_from = tomorrow, date_to = tomorrow)

    def test_project_slug(self):
        project = Project.objects.get(title='test project')
        self.assertEqual(project.slug, 'test-project')
    
    def test_project_status(self):
        self.assertEqual(self.current_project.project_status(), _('in progress'))
        self.assertEqual(self.past_project.project_status(), _('completed'))
        self.assertEqual(self.futur_project.project_status(), _('pending'))
        self.assertEqual(self.project_test.project_status(), _('pending'))

class ProjectResidencyTests(TestCase):
    
    def setUp(self):
        super(ProjectResidencyTests, self).setUp()
        self.project = ProjectResidency.objects.create(title='test project')
        self.project.save()
        self.event = Event.objects.create(title="mon-evenement", start=datetime.date.today(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        self.project.events = self.event
        self.residency_event = ProjectResidencyEvent.objects.create(residency = self.project, event = self.event)
        self.residency_event.save()

    def test_project_events(self):
        self.assertTrue(self.event in self.project.events)

class RepositoryTests(TestCase):

    def setUp(self):
        super(RepositoryTests,self).setUp()
        repository_system = RepositorySystem(name="repository",clone_command ="git clone https://github.com/Ircam-Web/Mezzo.git", pull_command="git pull" ,checkout_command ="git checkout", branch_command ="git branch")
        repository_system.save()
        self.repository = Repository.objects.create(system = repository_system, url = "https://github.com/Ircam-Web/Mezzo.git", name="mezzo")

    def test_repository_commands(self):
        self.assertEqual(self.repository.directory(),"oui")
