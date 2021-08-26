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

from organization.projects.models import *
from organization.network.models import *
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from organization.agenda.models import Event,EventLocation
from mezzanine.utils.tests import TestCase
from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.files.images import ImageFile
import tempfile
from django.core import urlresolvers
from unittest import skip

PROJECT_STATUS_CHOICES = (
    (0, _('rejected')),
    (1, _('pending')),
    (2, _('in process')),
    (3, _('accepted')),
)
class URLTests(TestCase):

    def setUp(self):
        super(URLTests, self).setUp()
        self.project_topic = ProjectTopic.objects.create(name="ICT",key="ICT")
        project_user = User.objects.filter(username="test").first()
        self.project_ict = Project.objects.create(title="ict project",topic=self.project_topic,validation_status=3)
        self.project_call = ProjectCall.objects.create(title="project call")
        self.project = Project.objects.create(title='django',content="django project",user=project_user,validation_status=1, call= self.project_call)
        self.project_demo = ProjectDemo.objects.create(title="django", project= self.project, url="https://wave.ircam.fr/demo/bachotheque/")
        self.project_blog_page = ProjectBlogPage.objects.create(project=self.project,content='django project blog page')
        self.project_residency = ProjectResidency.objects.create(project=self.project,validated=True)

    def test_projects_detail_url(self):
        response = self.client.get('/projects/detail/' + self.project.slug + "/")
        self.assertEqual(response.status_code,200)  
        self.assertContains(response,"django project") 
        self.assertTemplateUsed(response,'projects/project_detail.html')
        response = self.client.get('/project/detail/' + self.project.slug + "/")
        self.assertEqual(response.status_code,302)

    def test_projects_demo_url(self):
        response = self.client.get('/projects/demo/' + self.project_demo.slug + "/")
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'projects/project_demo_detail.html')
        response = self.client.get('/project/demo/' + self.project_demo.slug + "/")
        self.assertEqual(response.status_code,302)

    def test_projects_blog_page_url(self):
        response = self.client.get('/projects/blog/' + self.project_blog_page.slug + "/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"django project blog page") 
        self.assertTemplateUsed(response,'projects/project_blogpage_detail.html')
        response = self.client.get('/project/blog/' + self.project_blog_page.slug + "/")
        self.assertEqual(response.status_code,302)      

    def test_dynamic_content_project_view(self):
        response = self.client.get('/dynamic-content-project/')
        self.assertEqual(response.status_code,302)
        self.client.login(username="test",password="test")
        response = self.client.get('/dynamic-content-project/')
        self.assertEqual(response.status_code,200)        

    def test_ict_projects_list(self):
        response = self.client.get('/ict-projects/list/')      
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"projects/project_ict_list.html")
    
    def test_ict_projects_detail(self):
        response = self.client.get('/ict-projects/' + self.project_ict.slug + '/detail/')      
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"projects/project_ict_detail.html")

    def test_ict_projects_public(self):
        response = self.client.get('/calls/' + self.project_call.slug + '/projects/create/public/')      
        self.assertEqual(response.status_code,302)
        self.client.login(username="test",password="test")
        response = self.client.get('/calls/' + self.project_call.slug + '/projects/create/public/')      
        self.assertEqual(response.status_code,200)        
        self.assertTemplateUsed(response,"projects/project_ict_create_public_funding.html")
        
    def test_ict_edit_public(self):
        response = self.client.get('/profile/project/' + self.project.slug + '/')      
        self.assertEqual(response.status_code,302)
        self.client.login(username="test",password="test")
        response = self.client.get('/profile/project/' + self.project.slug + '/')      
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"projects/project_ict_edit_public_funding.html")

    @skip('404 error')
    def test_ict_edit_private(self):
        response = self.client.get('/profile/project/private/' + self.project.slug + '/')      
        self.assertEqual(response.status_code,302)
        self.client.login(username="test",password="test")
        response = self.client.get('/profile/project/private/' + self.project.slug + '/')      
        self.assertEqual(response.status_code,200)
        
    def test_project_residency_list(self):
        response = self.client.get('/calls/' + self.project_call.slug + '/residencies/list/')      
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"projects/project_residency_list.html")    

    def test_project_residency_detail_view(self):
        response = self.client.get('/calls/' + self.project_call.slug + '/residencies/' + self.project_residency.slug + '/detail/')      
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"projects/project_residency_detail.html")         

class ProjectTests(TestCase):

    def setUp(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        super(ProjectTests, self).setUp()
        app = "organization_projects"
        model = "project" 
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.project_program = ProjectProgram.objects.create()
        self.project_program_type = ProjectProgramType.objects.create()
        self.project_call = ProjectCall.objects.create()
        self.lead_team = Team.objects.create()
        self.lead_organization = Organization.objects.create()
        self.project_topic = ProjectTopic.objects.create()
        self.project = Project.objects.create(title='test project', type="internal", external_id="A12", program= self.project_program, program_type = self.project_program_type, call = self.project_call,
        lead_team = self.lead_team, lead_organization = self.lead_organization, website = "www.ircam.fr", topic = self.project_topic, is_archive = False, funding="public")
        self.current_project = Project.objects.create(title='current project',date_from = yesterday, date_to = tomorrow)
        self.past_project = Project.objects.create(title='past project',date_from = yesterday, date_to = yesterday)
        self.futur_project = Project.objects.create(title='futur project',date_from = tomorrow, date_to = tomorrow)

    def test_project_slug(self):
        self.assertEqual(self.project.slug, 'test-project')
    
    def test_project_status(self):
        self.assertEqual(self.current_project.project_status(), _('in progress'))
        self.assertEqual(self.past_project.project_status(), _('completed'))
        self.assertEqual(self.futur_project.project_status(), _('pending'))
        self.assertEqual(self.project.project_status(), _('pending'))

    def test_project_many_to_many_fields(self):
        team = Team.objects.create()
        self.project.teams.add(team)
        self.assertEquals(1,self.project.teams.all().count())        
        team = Team.objects.create()
        self.project.teams.add(team)
        self.assertEquals(2,self.project.teams.all().count())    

        organization = Organization.objects.create()
        self.project.organizations.add(organization)   
        self.assertEquals(1,self.project.organizations.all().count())
        organization = Organization.objects.create()
        self.project.organizations.add(organization)   
        self.assertEquals(2,self.project.organizations.all().count())

        person = Person.objects.create()
        self.project.referring_person.add(person)
        self.project.manager.add(person)
        self.assertEquals(1,self.project.referring_person.all().count())
        self.assertEquals(1,self.project.manager.all().count())
        person = Person.objects.create()
        self.project.referring_person.add(person)
        self.project.manager.add(person)
        self.assertEquals(2,self.project.referring_person.all().count())
        self.assertEquals(2,self.project.manager.all().count())

    def test_project_creation(self):
        self.assertTrue(isinstance(self.project,Project))
        self.assertEqual(self.project.title, "test project")
        self.assertEqual(self.project.type, "internal")
        self.assertEqual(self.project.external_id, "A12")
        self.assertEqual(self.project.program, self.project_program)
        self.assertEqual(self.project.program_type, self.project_program_type)
        self.assertEqual(self.project.call ,self.project_call)
        self.assertEqual(self.project.lead_team, self.lead_team)
        self.assertEqual(self.project.lead_organization, self.lead_organization)
        self.assertEqual(self.project.website, "www.ircam.fr")
        self.assertEqual(self.project.topic, self.project_topic)
        self.assertEqual(self.project.is_archive, False)
        self.assertEqual(self.project.funding, "public")
        self.assertEqual(self.project.validation_status, 1)

    def test_project_retrieval(self):
        self.assertTrue(self.project in Project.objects.all())
        self.assertTrue(self.project in Project.objects.filter(title="test project"))
        self.assertTrue(self.project in Project.objects.filter(type="internal"))
        self.assertTrue(self.project in Project.objects.filter(external_id="A12"))
        self.assertTrue(self.project in Project.objects.filter(program=self.project_program))
        self.assertTrue(self.project in Project.objects.filter(program_type=self.project_program_type))
        self.assertTrue(self.project in Project.objects.filter(call=self.project_call))
        self.assertTrue(self.project in Project.objects.filter(lead_team=self.lead_team))
        self.assertTrue(self.project in Project.objects.filter(lead_organization=self.lead_organization))
        self.assertTrue(self.project in Project.objects.filter(website="www.ircam.fr"))
        self.assertTrue(self.project in Project.objects.filter(topic=self.project_topic))
        self.assertTrue(self.project in Project.objects.filter(is_archive=False))
        self.assertTrue(self.project in Project.objects.filter(funding="public"))
        self.assertTrue(self.project in Project.objects.filter(validation_status=1))

    def test_project_update(self):
        self.project.external_id="A11"
        self.assertEqual(1,Project.objects.filter(external_id="A12").count())
        self.assertEqual(0,Project.objects.filter(external_id="A11").count())
        self.project.save()
        self.assertEqual(0,Project.objects.filter(external_id="A12").count())
        self.assertEqual(1,Project.objects.filter(external_id="A11").count()) 

    @skip("No translation")
    def test_project_deletion(self):
        project_work_package = ProjectWorkPackage.objects.create(project = self.project, number=2)
        project_playlist = ProjectPlaylist.objects.create(project = self.project)
        link_type = LinkType.objects.create(name = "test link")
        project_link = ProjectLink.objects.create(project = self.project,link_type=link_type)
        project_image = ProjectImage.objects.create(project = self.project)
        project_user_image = ProjectUserImage.objects.create(project = self.project)
        project_file = ProjectFile.objects.create(project = self.project)
        project_block = ProjectBlock.objects.create(project = self.project)
        project_demo = ProjectDemo.objects.create(project= self.project)
        project_related_title = ProjectRelatedTitle.objects.create(project = self.project)
        dynamic_content_project = DynamicContentProject.objects.create(project = self.project)
        project_blog_page = ProjectBlogPage.objects.create(project = self.project)
        project_contact = ProjectContact.objects.create(project = self.project)
        self.project.delete()
        self.assertFalse(project_work_package in ProjectWorkPackage.objects.all())
        self.assertTrue(project_playlist in ProjectPlaylist.objects.filter(project__isnull=True))
        self.assertTrue(project_link in ProjectLink.objects.filter(project__isnull=True))
        self.assertTrue(project_image in ProjectImage.objects.filter(project__isnull=True))
        self.assertTrue(project_user_image in ProjectUserImage.objects.filter(project__isnull=True))
        self.assertTrue(project_file in ProjectFile.objects.filter(project__isnull=True))
        self.assertTrue(project_block in ProjectBlock.objects.filter(project__isnull=True))
        self.assertTrue(project_demo in ProjectDemo.objects.filter(project__isnull=True))
        self.assertTrue(project_related_title in ProjectRelatedTitle.objects.filter(project__isnull=True))
        self.assertFalse(dynamic_content_project in DynamicContentProject.objects.all())
        self.assertTrue(project_blog_page in ProjectBlogPage.objects.filter(project__isnull=True))
        self.assertTrue(project_contact in ProjectContact.objects.filter(project__isnull=True))
        self.assertFalse(self.project in Project.objects.all())

    def test_project_fk_deletion(self):
        self.project_program.delete()
        self.assertTrue(self.project in Project.objects.filter(program__isnull=True))
        self.project_program_type.delete()
        self.assertTrue(self.project in Project.objects.filter(program_type__isnull=True))
        self.project_call.delete()
        self.assertTrue(self.project in Project.objects.filter(call__isnull=True))
        self.lead_team.delete()
        self.assertTrue(self.project in Project.objects.filter(lead_team__isnull=True))
        self.lead_organization.delete()
        self.assertTrue(self.project in Project.objects.filter(lead_organization__isnull=True))
        self.project_topic.delete()
        self.assertTrue(self.project in Project.objects.filter(topic__isnull=True))
        self.project.delete()

    def test_project_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/project_detail.html")

    @skip("No translation")
    def test_project_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)   
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)   

    @skip("No translation")
    def test_project_admin_creation(self):
        self.client.login(username='test', password='test')
        nb = Project.objects.count()
        response = self.client.post(self.url, {"title":'current project',"date_from" : '12/04/2018',"date_to": '12/05/2018'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nb+1,Project.objects.count())

    def test_project_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.project.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.project.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response,"editable")

class ProjectPublicDataTests(TestCase):
    
    def setUp(self):
        super(ProjectPublicDataTests, self).setUp()
        file = tempfile.NamedTemporaryFile(suffix='.png')
        img = ImageFile(file, name=file.name)
        self.project = Project.objects.create()
        self.project_public = ProjectPublicData.objects.create(project = self.project, brief_description="brief_description", challenges_description="challenges_description",technology_description="technology_description",
        objectives_description="objectives_description", resources_description="resources_description", implementation_start_date=datetime.date.today(), implementation_period = datetime.date.today() + datetime.timedelta(days=1),
        implementation_duration=datetime.date.today() + datetime.timedelta(days=1), image= img, image_credits="image_credits")

    def test_project_public_data_creation(self):
        self.assertTrue(isinstance(self.project_public,ProjectPublicData))
        self.assertEqual(self.project_public.project, self.project)
        self.assertEqual(self.project_public.brief_description, "brief_description")
        self.assertEqual(self.project_public.challenges_description, "challenges_description")
        self.assertEqual(self.project_public.technology_description, "technology_description")
        self.assertEqual(self.project_public.objectives_description, "objectives_description")
        self.assertEqual(self.project_public.resources_description, "resources_description")
        self.assertEqual(self.project_public.image_credits, "image_credits")

    def test_project_public_data_retrieval(self):
        self.assertTrue(self.project_public in ProjectPublicData.objects.all())
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(project= self.project))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(brief_description= "brief_description"))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(challenges_description= "challenges_description"))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(technology_description= "technology_description"))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(objectives_description= "objectives_description"))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(resources_description= "resources_description"))
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(image_credits= "image_credits"))

    def test_project_public_data_update(self):
        self.project_public.brief_description="brief_des"
        self.assertEqual(1,ProjectPublicData.objects.filter(brief_description="brief_description").count())
        self.assertEqual(0,ProjectPublicData.objects.filter(brief_description="brief_des").count())
        self.project_public.save()
        self.assertEqual(0,ProjectPublicData.objects.filter(brief_description="brief_description").count())
        self.assertEqual(1,ProjectPublicData.objects.filter(brief_description="brief_des").count()) 

    def test_project_public_data_fk_deletion(self):
        self.project.delete()
        self.assertTrue(self.project_public in ProjectPublicData.objects.filter(project__isnull=True))

class ProjectPrivateDataTests(TestCase):

    def setUp(self):
        super(ProjectPrivateDataTests, self).setUp()    
        file = tempfile.NamedTemporaryFile(suffix='.png')
        letter = ImageFile(file, name=file.name)
        self.project = Project.objects.create()
        self.project_private = ProjectPrivateData.objects.create(project = self.project, description="description", funding_programme="funding_programme", commitment_letter= letter, 
        investor_letter = letter, persons="persons", dimension="startup")

    def test_project_private_data_creation(self):
        self.assertTrue(isinstance(self.project_private,ProjectPrivateData))
        self.assertEqual(self.project_private.project, self.project)
        self.assertEqual(self.project_private.description, "description")        
        self.assertEqual(self.project_private.funding_programme, "funding_programme")        
        self.assertEqual(self.project_private.persons, "persons")        
        self.assertEqual(self.project_private.dimension, "startup")        

    def test_project_private_data_retrieval(self):
        self.assertTrue(self.project_private in ProjectPrivateData.objects.all())
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(project= self.project))
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(description= "description"))
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(funding_programme= "funding_programme"))
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(persons= "persons"))
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(dimension= "startup"))
    
    def test_project_private_data_update(self):
        self.project_private.description="des"
        self.assertEqual(1,ProjectPrivateData.objects.filter(description="description").count())
        self.assertEqual(0,ProjectPrivateData.objects.filter(description="des").count())
        self.project_private.save()
        self.assertEqual(0,ProjectPrivateData.objects.filter(description="description").count())
        self.assertEqual(1,ProjectPrivateData.objects.filter(description="des").count()) 

    def test_project_private_data_fk_deletion(self):
        self.project.delete()
        self.assertTrue(self.project_private in ProjectPrivateData.objects.filter(project__isnull=True))

class ProjectResidencyTests(TestCase):
    
    def setUp(self):
        super(ProjectResidencyTests, self).setUp()
        self.project_test = Project.objects.create()
        self.artist = Person.objects.create() 
        self.project = ProjectResidency.objects.create(project = self.project_test, artist = self.artist, validated = True, producer_commitment="producer_commitment")
        self.event = Event.objects.create(title="mon-evenement", start=datetime.date.today(), user=self._user, status=CONTENT_STATUS_PUBLISHED,publish_date=datetime.date.today())
        self.residency_event = ProjectResidencyEvent.objects.create(residency = self.project, event = self.event)
        self.article = Article.objects.create(title="Post", user=self._user, status=CONTENT_STATUS_PUBLISHED,publish_date=datetime.date.today())
        self.project_residency_article = ProjectResidencyArticle.objects.create(residency = self.project, article= self.article)

    def test_project_events(self):
        events = [re.event for re in self.project.residency_events.all()]
        self.assertTrue(self.event in events)
        self.assertTrue(self.event in self.project.events)

    def test_project_articles(self):
        articles = [ra.article for ra in self.project.residency_articles.all()]
        self.assertTrue(self.article in articles)
        self.assertTrue(self.article in self.project.articles)        

    def test_project_residency_creation(self):
        self.assertTrue(isinstance(self.project,ProjectResidency))
        self.assertEqual(self.project.project, self.project_test)
        self.assertEqual(self.project.artist, self.artist)
        self.assertEqual(self.project.validated, True)
        self.assertEqual(self.project.producer_commitment, "producer_commitment")

    def test_project_residency_retrieval(self):
        self.assertTrue(self.project in ProjectResidency.objects.all())
        self.assertTrue(self.project in ProjectResidency.objects.filter(project= self.project_test))
        self.assertTrue(self.project in ProjectResidency.objects.filter(artist= self.artist))
        self.assertTrue(self.project in ProjectResidency.objects.filter(validated= True))
        self.assertTrue(self.project in ProjectResidency.objects.filter(producer_commitment= "producer_commitment"))

    def test_project_residency_update(self):
        self.project.producer_commitment="producer_comm"
        self.assertEqual(1,ProjectResidency.objects.filter(producer_commitment="producer_commitment").count())
        self.assertEqual(0,ProjectResidency.objects.filter(producer_commitment="producer_comm").count())
        self.project.save()
        self.assertEqual(0,ProjectResidency.objects.filter(producer_commitment="producer_commitment").count())
        self.assertEqual(1,ProjectResidency.objects.filter(producer_commitment="producer_comm").count())         

    def test_project_residency_fk_deletion(self):
        self.project_test.delete()
        self.assertTrue(self.project in ProjectResidency.objects.filter(project__isnull=True))
        self.artist.delete()
        self.assertTrue(self.project in ProjectResidency.objects.filter(artist__isnull=True))

    def test_project_residency_deletion(self): 
        project_residency_producer = ProjectResidencyProducer.objects.create(residency = self.project)
        project_residency_file = ProjectResidencyFile.objects.create(residency = self.project)
        project_residency_image = ProjectResidencyImage.objects.create(residency= self.project)
        project_residency_user_image = ProjectResidencyUserImage.objects.create(residency = self.project)
        self.project.delete()
        self.assertTrue(project_residency_producer in ProjectResidencyProducer.objects.filter(residency__isnull=True))
        self.assertTrue(project_residency_file in ProjectResidencyFile.objects.filter(residency__isnull=True))
        self.assertTrue(project_residency_image in ProjectResidencyImage.objects.filter(residency__isnull=True))
        self.assertTrue(project_residency_user_image in ProjectResidencyUserImage.objects.filter(residency__isnull=True))
        self.assertTrue(self.project_residency_article in ProjectResidencyArticle.objects.filter(residency__isnull=True))
        self.assertTrue(self.residency_event in ProjectResidencyEvent.objects.filter(residency__isnull=True))        
        self.assertFalse(self.project in ProjectResidency.objects.all())        