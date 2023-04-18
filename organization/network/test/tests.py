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

from django.test import SimpleTestCase, TestCase
from mezzanine.utils.tests import TestCase as TC
from django.core import management
from io import StringIO
from organization.network.utils import get_nb_half_days_by_period,\
    get_nb_half_days_by_period_per_month
from organization.network.api import get_leave_days_per_month
import ast
from organization.network.models import Person, Organization, Department, Team,\
    PersonActivity, DepartmentPage, MediaDepartment, TeamLink, OrganizationType,\
    OrganizationRole, OrganizationLinkedBlockInline, OrganizationLinkedInline,\
    OrganizationPlaylist, OrganizationLink, OrganizationImage, OrganizationBlock,\
    OrganizationService, OrganizationEventLocation, OrganizationContact,\
    OrganizationUserImage, ProducerData, PersonPlaylist, PersonImage, PersonFile,\
    PersonBlock, PersonLink, PersonListBlockInline
from organization.pages.models import TeamPage
from organization.media.models import Media
from datetime import datetime
from django.core.files.images import ImageFile
import tempfile
from django.core import urlresolvers
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED, LinkType
from unittest import skip
from unittest import skipIf
from django.conf import settings

#
# To run tests without database :
# python manage.py test organization.network.test.tests_back.[class_name].[method_name] --settings='organization.core.no_db_settings'  # noqa: E501
#


class URLTests(TC):

    def setUp(self):
        super(URLTests, self).setUp()
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            username="basic_user",
            email="email",
            password="basic_user"
        )
        self.person = Person.objects.create(
            user=self.user,
            person_title="basic_user"
        )

    @skipIf(not hasattr(settings, 'TIMESHEET_START'), 'Ensure setting is set')
    def test_person_timesheet_url(self):
        response = self.client.get('/person/timesheet/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.client.login(username="basic_user", password="basic_user")
        response = self.client.get('/person/timesheet/')
        self.assertEqual(response.status_code, 200)

    def test_person_detail_url(self):
        response = self.client.get('/person/' + self.person.slug + "/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/person_detail.html')

    def test_profile_detail_url(self):
        response = self.client.get('/profile/' + self.person.user.username + "/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/person_detail.html')

    def test_person_list_url(self):
        response = self.client.get('/person/list/')
        self.assertTemplateUsed(response, 'network/person_list.html')

    def test_person_list_block_autocomplete_url(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/person-list-block-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_person_autocomplete_url(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/person-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_network_url(self):
        response = self.client.get('/network/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/organization_list.html')

    def test_organization_linked_list_autocomplete(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/organization-linked-list-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_organization_linked_autocomplete(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/organization-linked-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_person_activity_autocomplete(self):
        response = self.client.get('/person-activity-autocomplete/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='test', password='test')
        response = self.client.get('/person-activity-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_work_packages_autocomplete(self):
        response = self.client.get('/work-packages-autocomplete/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='test', password='test')
        response = self.client.get('/work-packages-autocomplete/')
        self.assertEqual(response.status_code, 200)

    def test_producers_submission(self):
        self.client.login(username="test", password="test")
        response = self.client.get('/producers/submission/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/organization_producer_create.html')

    def test_producers_list(self):
        response = self.client.get('/producers/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/organization_producer_list.html')

    def test_jury_list(self):
        response = self.client.get('/jury/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/organization_jury_list.html')


class NetworkTests(TC):

    def setUp(self):
        super(NetworkTests, self).setUp()
        self.organization = Organization(name="my_organization")
        self.organization.save()
        self.department = Department.objects.create(
            name="my_department",
            organization=self.organization
        )
        self.parent_team = Team.objects.create(
            name="team1",
            organization=self.organization,
            department=self.department
        )
        self.team = Team.objects.create(
            name="team2",
            organization=self.organization,
            department=self.department,
            parent=self.parent_team
        )
        self.person = Person.objects.create()
        self.person_activity = PersonActivity.objects.create(person=self.person)
        self.person_activity.organizations.add(self.organization)

    def test_network_dependencies(self):
        self.assertEqual(self.department.organization.name, "my_organization")
        self.assertEqual(self.team.department.name, "my_department")
        self.assertEqual(self.team.organization.name, "my_organization")
        self.assertEqual(self.team.parent.name, "team1")
        self.assertEqual(
            self.person.activities.all()[0].organizations.all()[0].name,
            "my_organization"
        )


class DepartmentTests(TC):

    def setUp(self):
        super(DepartmentTests, self).setUp()
        app = "organization_network"
        model = "department"
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.organization = Organization.objects.create(name="orga")
        self.department = Department.objects.create(
            name="my department",
            organization=self.organization
        )
        self.department_page = DepartmentPage.objects.create(
            title="title department",
            content="my dep content",
            publish_date=datetime.today(),
            department=self.department,
            status=CONTENT_STATUS_PUBLISHED
        )

    @skip("error : title_fr not in list")
    def test_department_display_for_everyone(self):
        self.client.logout()
        response = self.client.get("/title-department/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/departmentpage.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.department_page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/departmentpage.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.department_page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/departmentpage.html")

    def test_department_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_department_admin_creation(self):
        self.client.login(username='test', password='test')
        nb = Department.objects.count()
        response = self.client.post(
            self.url,
            {
                "name": 'department',
                "organization": self.organization.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nb+1, Department.objects.count())

    @skip("error : title_fr not in list")
    def test_department_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.department_page.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.department_page.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.department_page.get_absolute_url())
        self.assertContains(response, "editable")

    def test_department_fk_deletion(self):
        self.organization.delete()
        self.assertFalse(self.department in Department.objects.all())

    def test_department_creation(self):
        self.assertTrue(isinstance(self.department, Department))
        self.assertEqual(self.department.organization, self.organization)
        self.assertEqual(self.department.name, "my department")

    def test_department_retrieval(self):
        self.assertTrue(
            self.department in Department.objects.filter(
                organization=self.organization
            )
        )
        self.assertTrue(
            self.department in Department.objects.filter(
                name="my department"
            )
        )

    def test_department_update(self):
        self.department.name = "my dep"
        self.assertEqual(1, Department.objects.filter(name="my department").count())
        self.assertEqual(0, Department.objects.filter(name="my dep").count())
        self.department.save()
        self.assertEqual(0, Department.objects.filter(name="my department").count())
        self.assertEqual(1, Department.objects.filter(name="my dep").count())

    def test_department_deletion(self):
        department_page = DepartmentPage.objects.create(department=self.department)
        media_test = Media.objects.create()
        media_department = MediaDepartment.objects.create(
            department=self.department,
            media=media_test
        )
        self.department.delete()
        self.assertFalse(self.department in Department.objects.all())
        self.assertTrue(
            department_page in DepartmentPage.objects.filter(
                department__isnull=True
            )
        )
        self.assertTrue(
            media_department in MediaDepartment.objects.filter(
                department__isnull=True
            )
        )


class TeamTests(TC):

    def setUp(self):
        super(TeamTests, self).setUp()
        app = "organization_network"
        model = "team"
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.organization = Organization.objects.create()
        self.department = Department.objects.create(
            name="my_department",
            organization=self.organization
        )
        self.parent_team = Team.objects.create()
        self.team = Team.objects.create(
            organization=self.organization,
            department=self.department,
            code="A10",
            is_legacy=True,
            parent=self.parent_team,
            hal_tutelage="hal_tutelage",
            hal_researche_structure="hal_researche_structure"
        )
        self.team_page = TeamPage.objects.create(team=self.team)

    def test_team_fk_deletion(self):
        self.organization.delete()
        self.department.delete()
        self.parent_team.delete()
        self.assertTrue(self.team in Team.objects.filter(organization__isnull=True))
        self.assertTrue(self.team in Team.objects.filter(department__isnull=True))
        self.assertTrue(self.team in Team.objects.filter(parent__isnull=True))

    @skip("Translation error")
    def test_team_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "magazine/article/article_detail.html")

    def test_team_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @skip("Translation error")
    def test_team_admin_creation(self):
        self.client.login(username='test', password='test')
        nb = Team.objects.count()
        response = self.client.post(self.url, {"name": 'team'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nb+1, Team.objects.count())

    @skip("Translation error")
    def test_team_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.team_page.get_absolute_url())
        self.assertContains(response, "editable")

    def test_team_creation(self):
        self.assertTrue(isinstance(self.team, Team))
        self.assertEqual(self.team.organization, self.organization)
        self.assertEqual(self.team.department, self.department)
        self.assertEqual(self.team.code, "A10")
        self.assertEqual(self.team.is_legacy, True)
        self.assertEqual(self.team.parent, self.parent_team)
        self.assertEqual(self.team.hal_tutelage, "hal_tutelage")
        self.assertEqual(self.team.hal_researche_structure, "hal_researche_structure")

    def test_team_retrieval(self):
        self.assertTrue(
            self.team in Team.objects.filter(organization=self.organization)
        )
        self.assertTrue(self.team in Team.objects.filter(department=self.department))
        self.assertTrue(self.team in Team.objects.filter(code="A10"))
        self.assertTrue(self.team in Team.objects.filter(is_legacy=True))
        self.assertTrue(self.team in Team.objects.filter(parent=self.parent_team))
        self.assertTrue(self.team in Team.objects.filter(hal_tutelage="hal_tutelage"))
        self.assertTrue(
            self.team in Team.objects.filter(
                hal_researche_structure="hal_researche_structure"
            )
        )

    def test_team_update(self):
        self.team.code = "B12"
        self.assertEqual(1, Team.objects.filter(code="A10").count())
        self.assertEqual(0, Team.objects.filter(code="B12").count())
        self.team.save()
        self.assertEqual(0, Team.objects.filter(code="A10").count())
        self.assertEqual(1, Team.objects.filter(code="B12").count())

    def test_team_deletion(self):
        team_page = TeamPage.objects.create(team=self.team)
        link_type = LinkType.objects.create(name="test link")
        team_link = TeamLink.objects.create(team=self.team, link_type=link_type)
        self.team.delete()
        self.assertEqual(0, Team.objects.filter(hal_tutelage="hal_tutelage").count())
        self.assertTrue(team_page in TeamPage.objects.filter(team__isnull=True))
        self.assertTrue(team_link in TeamLink.objects.filter(team__isnull=True))


class OrganizationTests(TC):

    def setUp(self):
        super(OrganizationTests, self).setUp()
        app = "organization_network"
        model = "organization"
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.organization_type = OrganizationType.objects.create(
            name="organization_type"
        )
        self.organization_role = OrganizationRole.objects.create(
            name="organization_role",
            key="OR"
        )
        self.organization = Organization.objects.create(
            type=self.organization_type,
            role=self.organization_role,
            email="organization@test.fr",
            initials="ORGNZT",
            is_on_map=True,
            is_host=True,
            telephone="0101010101",
            opening_times="daytime",
            subway_access="subway_access",
            bio="bio"
        )

    def test_organization_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.organization.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/organization_list.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.organization.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/organization_list.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.organization.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/organization_list.html")

    def test_organization_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_organization_admin_creation(self):
        self.client.login(username='test', password='test')
        nb = Organization.objects.count()
        response = self.client.post(
            self.url,
            {
                "name": 'organization',
                'blocks-INITIAL_FORMS': '0',
                'blocks-TOTAL_FORMS': '1',
                'event_locations-INITIAL_FORMS': '0',
                'event_locations-TOTAL_FORMS': '1',
                'images-INITIAL_FORMS': '0',
                'images-TOTAL_FORMS': '1',
                'links-INITIAL_FORMS': '0',
                'links-TOTAL_FORMS': '1',
                'organization_linked_block-INITIAL_FORMS': '0',
                'organization_linked_block-TOTAL_FORMS': '1',
                'playlists-INITIAL_FORMS': '0',
                'playlists-TOTAL_FORMS': '1',
                'producer_data-INITIAL_FORMS': '0',
                'producer_data-TOTAL_FORMS': '1',
                'services-0-box_size': '3',
                'services-INITIAL_FORMS': '0',
                'services-TOTAL_FORMS': '1',
                'validation_status': '1'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nb+1, Organization.objects.count())

    def test_organization_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.organization.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.organization.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.organization.get_absolute_url())
        self.assertContains(response, "editable")

    def test_organization_fk_deletion(self):
        self.organization_type.delete()
        self.organization_role.delete()
        self.assertTrue(
            self.organization in Organization.objects.filter(type__isnull=True)
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(role__isnull=True)
        )

    def test_organization_creation(self):
        self.assertTrue(isinstance(self.organization, Organization))
        self.assertEqual(self.organization.type, self.organization_type)
        self.assertEqual(self.organization.role, self.organization_role)
        self.assertEqual(self.organization.initials, "ORGNZT")
        self.assertEqual(self.organization.email, "organization@test.fr")
        self.assertEqual(self.organization.telephone, "0101010101")
        self.assertEqual(self.organization.bio, "bio")
        self.assertEqual(self.organization.is_on_map, True)
        self.assertEqual(self.organization.is_host, True)
        self.assertEqual(self.organization.opening_times, "daytime")
        self.assertEqual(self.organization.subway_access, "subway_access")
        self.assertEqual(self.organization.admin_thumb_type, "logo")
        self.assertEqual(self.organization.validation_status, 1)

    def test_organization_retrieval(self):
        self.assertTrue(
            self.organization in Organization.objects.filter(
                type=self.organization_type
            )
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(
                role=self.organization_role
            )
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(initials="ORGNZT")
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(
                email="organization@test.fr"
            )
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(telephone="0101010101")
        )
        self.assertTrue(self.organization in Organization.objects.filter(bio="bio"))
        self.assertTrue(
            self.organization in Organization.objects.filter(is_on_map=True)
        )
        self.assertTrue(self.organization in Organization.objects.filter(is_host=True))
        self.assertTrue(
            self.organization in Organization.objects.filter(opening_times="daytime")
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(
                subway_access="subway_access"
            )
        )
        self.assertTrue(
            self.organization in Organization.objects.filter(
                validation_status=1
            )
        )

    def test_organization_update(self):
        self.organization.email = "organization@organization.fr"
        self.assertEqual(
            1,
            Organization.objects.filter(email="organization@test.fr").count()
        )
        self.assertEqual(
            0,
            Organization.objects.filter(email="organization@organization.fr").count()
        )
        self.organization.save()
        self.assertEqual(
            0,
            Organization.objects.filter(email="organization@test.fr").count()
        )
        self.assertEqual(
            1,
            Organization.objects.filter(email="organization@organization.fr").count()
        )

    def test_organization_deletion(self):
        file = tempfile.NamedTemporaryFile(suffix='.png')
        img = ImageFile(file, name=file.name)
        self.organization_type.delete()
        self.assertTrue(
            self.organization in Organization.objects.filter(type__isnull=True)
        )
        self.organization_role.delete()
        self.assertTrue(
            self.organization in Organization.objects.filter(role__isnull=True)
        )
        organization_linked_block_inline = OrganizationLinkedBlockInline.objects.create(
            title="organization_linked_block_inline",
            organization_main=self.organization
        )
        organization_linked_inline = OrganizationLinkedInline.objects.create(
            title="organization_linked_inline",
            organization=self.organization
        )
        organization_playlist = OrganizationPlaylist.objects.create(
            organization=self.organization
        )
        link_type = LinkType.objects.create(name="test link")
        organization_link = OrganizationLink.objects.create(
            organization=self.organization,
            link_type=link_type
        )
        organization_image = OrganizationImage.objects.create(
            organization=self.organization
        )
        organization_block = OrganizationBlock.objects.create(
            organization=self.organization
        )
        organization_service = OrganizationService.objects.create(
            organization=self.organization,
            image=img
        )
        organization_event_location = OrganizationEventLocation.objects.create(
            organization=self.organization
        )
        organization_contact = OrganizationContact.objects.create(
            organization=self.organization
        )
        organization_user_image = OrganizationUserImage.objects.create(
            organization=self.organization
        )
        producer_data = ProducerData.objects.create(
            organization=self.organization,
            experience_description="experience_description",
            producer_description="producer_description"
        )
        self.organization.delete()
        self.assertEqual(
            0,
            Organization.objects.filter(email="organization@test.fr").count()
        )
        self.assertTrue(
            organization_linked_block_inline in OrganizationLinkedBlockInline.objects
            .filter(organization_main__isnull=True)
        )
        self.assertTrue(
            organization_playlist in OrganizationPlaylist.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_link in OrganizationLink.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_image in OrganizationImage.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_block in OrganizationBlock.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_linked_inline in OrganizationLinkedInline.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_service in OrganizationService.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_event_location in OrganizationEventLocation.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_contact in OrganizationContact.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            organization_user_image in OrganizationUserImage.objects
            .filter(organization__isnull=True)
        )
        self.assertTrue(
            producer_data in ProducerData.objects
            .filter(organization__isnull=True)
        )


class PersonTests(TC):

    def setUp(self):
        super(PersonTests, self).setUp()
        app = "organization_network"
        model = "person"
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            username="user",
            password="pswd"
        )
        self.person = Person.objects.create(
            first_name="Jean",
            last_name="Dupont",
            user=self.user,
            gender="male",
            email="test@test.fr",
            telephone="0606060606",
            bio="my bio",
            role="my role"
        )
        self.person.save()
        self.person2 = Person.objects.create(title="Jean Dupont")
        self.person2.set_names()

    def test_person_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.person.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/person_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.person.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/person_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.person.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "network/person_detail.html")

    def test_person_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_person_admin_creation(self):
        self.client.login(username='test', password='test')
        nb = Person.objects.count()
        response = self.client.post(
            self.url,
            {
                "title": 'title',
                'activities-INITIAL_FORMS': '0',
                'activities-TOTAL_FORMS': '1',
                'blocks-INITIAL_FORMS': '0',
                'blocks-TOTAL_FORMS': '1',
                'files-INITIAL_FORMS': '0',
                'files-TOTAL_FORMS': '1',
                'images-INITIAL_FORMS': '0',
                'images-TOTAL_FORMS': '1',
                'links-INITIAL_FORMS': '0',
                'links-TOTAL_FORMS': '1',
                'playlists-INITIAL_FORMS': '0',
                'playlists-TOTAL_FORMS': '1',
                'status': '2'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nb+1, Person.objects.count())

    def test_person_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.person.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.person.get_absolute_url())
        self.assertNotContains(response, "editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.person.get_absolute_url())
        self.assertContains(response, "editable")

    def test_person_title(self):
        self.assertEqual(self.person2.first_name, "Jean")
        self.assertEqual(self.person2.last_name, "Dupont")
        self.assertEqual(self.person.title, "Jean Dupont")

    def test_person_can_have_several_activities(self):
        person_activities = []
        person_activities.append(PersonActivity.objects.create(person=self.person))
        person_activities.append(PersonActivity.objects.create(person=self.person))
        person_activities.append(PersonActivity.objects.create(person=self.person))
        for person_activity in person_activities:
            self.assertTrue(person_activity in self.person.activities.all())

    def test_person_creation(self):
        self.assertTrue(isinstance(self.person, Person))
        self.assertEqual(self.person.first_name, "Jean")
        self.assertEqual(self.person.last_name, "Dupont")
        self.assertEqual(self.person.user, self.user)
        self.assertEqual(self.person.gender, "male")
        self.assertEqual(self.person.email, "test@test.fr")
        self.assertEqual(self.person.telephone, "0606060606")
        self.assertEqual(self.person.bio, "my bio")
        self.assertEqual(self.person.role, "my role")

    def test_person_retrieval(self):
        self.assertTrue(self.person in Person.objects.filter(first_name="Jean"))
        self.assertTrue(self.person in Person.objects.filter(last_name="Dupont"))
        self.assertTrue(self.person in Person.objects.filter(user=self.user))
        self.assertTrue(self.person in Person.objects.filter(gender="male"))
        self.assertTrue(self.person in Person.objects.filter(email="test@test.fr"))
        self.assertTrue(self.person in Person.objects.filter(telephone="0606060606"))
        self.assertTrue(self.person in Person.objects.filter(bio="my bio"))
        self.assertTrue(self.person in Person.objects.filter(role="my role"))

    def test_person_update(self):
        self.person.telephone = "0707070707"
        self.assertEqual(1, Person.objects.filter(telephone="0606060606").count())
        self.assertEqual(0, Person.objects.filter(telephone="0707070707").count())
        self.person.save()
        self.assertEqual(0, Person.objects.filter(telephone="0606060606").count())
        self.assertEqual(1, Person.objects.filter(telephone="0707070707").count())

    def test_person_deletion(self):
        person_playlist = PersonPlaylist.objects.create(person=self.person)
        person_image = PersonImage.objects.create(person=self.person)
        person_file = PersonFile.objects.create(person=self.person)
        person_block = PersonBlock.objects.create(person=self.person)
        link_type = LinkType.objects.create(name="test link")
        person_link = PersonLink.objects.create(
            person=self.person,
            link_type=link_type
        )
        person_list_block_inline = PersonListBlockInline.objects.create(
            person=self.person
        )
        self.person.delete()
        self.assertEqual(0, Person.objects.filter(bio="my bio").count())
        self.assertTrue(
            person_playlist in PersonPlaylist.objects.filter(person__isnull=True)
        )
        self.assertTrue(person_image in PersonImage.objects.filter(person__isnull=True))
        self.assertTrue(person_file in PersonFile.objects.filter(person__isnull=True))
        self.assertTrue(person_block in PersonBlock.objects.filter(person__isnull=True))
        self.assertTrue(person_link in PersonLink.objects.filter(person__isnull=True))
        self.assertTrue(
            person_list_block_inline in PersonListBlockInline.objects.filter(
                person__isnull=True
            )
        )

    def test_person_fk_deletion(self):
        self.user.delete()
        self.assertTrue(self.person in Person.objects.all())


class Timesheet(TestCase):

    def setUp(self):
        self.resulted_person = StringIO()
        # id of persons who as to enter its timesheet
        self.expected_person = [2, 64, 70, 77, 83, 96, 132,
                                137, 156, 167, 171, 173, 174,
                                248, 355, 442, 497, 646, 656,
                                823, 849, 861, 887, 888]
        self.date_from = "2017/03/01"
        self.date_to = "2017/03/31"

    @skipIf(not hasattr(settings, 'TIMESHEET_LOG_PATH'), 'Ensure setting is set')
    def test_person_has_to_enter_timesheet(self):
        management.call_command(
            "timesheetmail",
            input_from=self.date_from,
            input_to=self.date_to,
            stdout=self.resulted_person
        )
        self.assertListEqual(
            ast.literal_eval(self.resulted_person.getvalue()), self.expected_person
        )
        self.resulted_person.close()


class NbOfHalfDaysInPeriodTestCase(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2016, 12, 1)
        self.date_to = datetime.date(2016, 12, 31)

    def test_nbhalf_half_days(self):

        expected = {
          "monday_am": 4,
          "monday_pm": 4,
          "tuesday_am": 4,
          "tuesday_pm": 4,
          "wednesday_am": 4,
          "wednesday_pm": 4,
          "thursday_am": 5,
          "thursday_pm": 5,
          "friday_am": 5,
          "friday_pm": 5,
        }

        result = get_nb_half_days_by_period(self.date_from, self.date_to)
        self.assertEquals(result, expected)


class NbOfHalfDaysInPeriodPerMonthTestCase(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2015, 1, 1)
        self.date_to = datetime.date(2015, 12, 31)

    @skipIf(not hasattr(settings, 'FIGGO_API_URL_PROD'), 'Ensure setting is set')
    def test_nbhalf_half_days(self):

        expected = {
           1: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           2: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           3: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           4: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           5: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           6: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           7: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           8: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           9: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           10: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           11: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           },
           12: {
              'friday_pm': 52,
              'tuesday_am': 52,
              'thursday_pm': 53,
              'monday_pm': 52,
              'tuesday_pm': 52,
              'wednesday_am': 52,
              'thursday_am': 53,
              'wednesday_pm': 52,
              'friday_am': 52,
              'monday_am': 52
           }
        }

        result = get_nb_half_days_by_period_per_month(self.date_from, self.date_to)
        self.assertEquals(result, expected)


class NbOfHalfDaysInPeriodPerMonthTestCase2(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2016, 1, 1)
        self.date_to = datetime.date(2016, 12, 31)

    def test_nbhalf_half_days(self):
        expected = {
               1: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 4,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 4,
                  'wednesday_am': 4,
                  'thursday_pm': 4,
                  'friday_pm': 4,
                  'monday_pm': 4
               },
               2: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 4,
                  'monday_am': 5,
                  'tuesday_pm': 4,
                  'friday_am': 4,
                  'wednesday_am': 4,
                  'thursday_pm': 4,
                  'friday_pm': 4,
                  'monday_pm': 5
               },
               3: {
                  'wednesday_pm': 5,
                  'tuesday_am': 5,
                  'thursday_am': 5,
                  'monday_am': 3,
                  'tuesday_pm': 5,
                  'friday_am': 4,
                  'wednesday_am': 5,
                  'thursday_pm': 5,
                  'friday_pm': 4,
                  'monday_pm': 3
               },
               4: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 4,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 5,
                  'wednesday_am': 4,
                  'thursday_pm': 4,
                  'friday_pm': 5,
                  'monday_pm': 4
               },
               5: {
                  'wednesday_pm': 4,
                  'tuesday_am': 5,
                  'thursday_am': 3,
                  'monday_am': 4,
                  'tuesday_pm': 5,
                  'friday_am': 4,
                  'wednesday_am': 4,
                  'thursday_pm': 3,
                  'friday_pm': 4,
                  'monday_pm': 4
               },
               6: {
                  'wednesday_pm': 5,
                  'tuesday_am': 4,
                  'thursday_am': 5,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 4,
                  'wednesday_am': 5,
                  'thursday_pm': 5,
                  'friday_pm': 4,
                  'monday_pm': 4
               },
               7: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 3,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 5,
                  'wednesday_am': 4,
                  'thursday_pm': 3,
                  'friday_pm': 5,
                  'monday_pm': 4
               },
               8: {
                  'wednesday_pm': 5,
                  'tuesday_am': 5,
                  'thursday_am': 4,
                  'monday_am': 4,
                  'tuesday_pm': 5,
                  'friday_am': 4,
                  'wednesday_am': 5,
                  'thursday_pm': 4,
                  'friday_pm': 4,
                  'monday_pm': 4
               },
               9: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 5,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 5,
                  'wednesday_am': 4,
                  'thursday_pm': 5,
                  'friday_pm': 5,
                  'monday_pm': 4
               },
               10: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 4,
                  'monday_am': 5,
                  'tuesday_pm': 4,
                  'friday_am': 4,
                  'wednesday_am': 4,
                  'thursday_pm': 4,
                  'friday_pm': 4,
                  'monday_pm': 5
               },
               11: {
                  'wednesday_pm': 5,
                  'tuesday_am': 4,
                  'thursday_am': 4,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 3,
                  'wednesday_am': 5,
                  'thursday_pm': 4,
                  'friday_pm': 3,
                  'monday_pm': 4
               },
               12: {
                  'wednesday_pm': 4,
                  'tuesday_am': 4,
                  'thursday_am': 5,
                  'monday_am': 4,
                  'tuesday_pm': 4,
                  'friday_am': 5,
                  'wednesday_am': 4,
                  'thursday_pm': 5,
                  'friday_pm': 5,
                  'monday_pm': 4
               }
            }
        result = get_nb_half_days_by_period_per_month(self.date_from, self.date_to)
        self.assertEquals(result, expected)


class NbOfLeaveDaysPerMonthTestCase4(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2017, 5, 1)
        self.date_to = datetime.date(2017, 5, 31)
        self.external_id = 185  # Emilie Zawadzki

    @skipIf(not hasattr(settings, 'FIGGO_API_URL_PROD'), 'Ensure setting is set')
    def test_nb_leave_days(self):
        expected = {}
        result = get_leave_days_per_month(
            self.date_from,
            self.date_to,
            self.external_id
        )
        self.assertEquals(result, expected)


class NbOfLeaveDaysPerMonthTestCase3(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2016, 1, 1)
        self.date_to = datetime.date(2016, 1, 31)
        self.external_id = 162  # Olivier Houix

    @skipIf(not hasattr(settings, 'FIGGO_API_URL_PROD'), 'Ensure setting is set')
    def test_nb_leave_days(self):
        expected = {}
        result = get_leave_days_per_month(
            self.date_from, self.date_to, self.external_id
        )
        self.assertEquals(result, expected)


class NbOfLeaveDaysPerMonthTestCase2(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2016, 1, 1)
        self.date_to = datetime.date(2016, 1, 31)
        self.external_id = 106  # Hugues Vinet

    @skipIf(
        not hasattr(
            settings,
            'FIGGO_API_URL_PROD'
        ),
        'Ensure setting is set'
    )
    def test_nb_leave_days(self):
        expected = {}
        result = get_leave_days_per_month(
            self.date_from,
            self.date_to,
            self.external_id
        )
        self.assertEquals(result, expected)


class NbOfLeaveDaysPerMonthTestCase(SimpleTestCase):

    def setUp(self):
        import datetime
        self.date_from = datetime.date(2015, 1, 1)
        self.date_to = datetime.date(2015, 12, 31)
        self.external_id = 97  # Norber Schnell

    @skipIf(
        not hasattr(
            settings,
            'FIGGO_API_URL_PROD'
        ),
        'Ensure setting is set'
    )
    def test_nb_leave_days(self):

        expected = {
           1: {
              'wednesday_am': 1,
              'monday_am': 2,
              'friday_am': 1,
              'thursday_am': 1,
              'tuesday_pm': 1,
              'wednesday_pm': 1,
              'friday_pm': 2,
              'tuesday_am': 1,
              'monday_pm': 2,
              'thursday_pm': 1
           },
           6: {
              'monday_pm': 1
           },
           7: {
              'wednesday_am': 3,
              'monday_am': 2,
              'friday_am': 2,
              'thursday_am': 3,
              'tuesday_pm': 2,
              'wednesday_pm': 3,
              'friday_pm': 2,
              'tuesday_am': 2,
              'monday_pm': 2,
              'thursday_pm': 3
           },
           8: {
              'wednesday_am': 2,
              'monday_am': 3,
              'friday_am': 2,
              'thursday_am': 2,
              'tuesday_pm': 3,
              'wednesday_pm': 2,
              'friday_pm': 2,
              'tuesday_am': 3,
              'monday_pm': 4,
              'thursday_pm': 2
           },
           9: {
              'wednesday_am': 1,
              'friday_am': 1,
              'thursday_am': 1,
              'tuesday_pm': 1,
              'wednesday_pm': 1,
              'tuesday_am': 1,
              'friday_pm': 1,
              'thursday_pm': 1
           },
           10: {
              'thursday_pm': 1
           },
           11: {
              'wednesday_am': 1,
              'monday_am': 1,
              'tuesday_pm': 1,
              'wednesday_pm': 1,
              'friday_pm': 1,
              'tuesday_am': 1,
              'monday_pm': 1
           },
           12: {
              'wednesday_am': 2,
              'monday_am': 1,
              'thursday_am': 2,
              'tuesday_pm': 2,
              'wednesday_pm': 2,
              'monday_pm': 2,
              'tuesday_am': 2,
              'thursday_pm': 2
           }
        }

        result = get_leave_days_per_month(
            self.date_from,
            self.date_to,
            self.external_id
        )
        self.assertEquals(result, expected)
