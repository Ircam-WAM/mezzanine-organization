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

from mezzanine.utils.tests import TestCase
from organization.job.models import *
from organization.job.admin import *
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import urlresolvers
from django.forms import BaseFormSet
from django.forms import formset_factory
from django.contrib.auth import get_user_model as User

class URLTests(TestCase):

    def setUp(self):
        super(URLTests, self).setUp()
        self.job_offer = JobOffer.objects.create(title="django dev",email = "testing@email.fr", type="internship", content = "python")
        self.candidacy = Candidacy.objects.create(title="research", text_button_external="more") 

    def test_job_offer_detail_url(self):
        response = self.client.get('/job-offer/' + self.job_offer.slug + "/")
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "python")  
        self.assertTemplateUsed(response,"job/job_offer_detail.html")

    def test_basic_job_offer_url(self):
        response = self.client.get('/job-offer/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "django-dev")
        self.assertTemplateUsed(response,"job/job_offer_list.html")

    def test_basic_candidacies_url(self):
        response = self.client.get('/candidacies/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "research")
        self.assertTemplateUsed(response,"job/candidacy_list.html")

    def test_candidacies_autocomplete(self):
        response = self.client.get('/candidacy-autocomplete/')
        self.assertEqual(response.status_code,200)

class JobOfferTests(TestCase):

    def setUp(self):
        super(JobOfferTests, self).setUp()
        app = "organization-job"
        model = "joboffer" 
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.file = SimpleUploadedFile('letter.txt'.encode(), 'content'.encode())
        self.job_offer = JobOffer.objects.create(email = "test@test.fr", type="internship")
        self.job_response = JobResponse.objects.create(first_name = "jean", last_name = "dupont", email="jean@dupont.fr" , message="I want this job", 
        curriculum_vitae = self.file, cover_letter = self.file, job_offer = self.job_offer)

    def test_job_offer_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job/job_offer_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job/job_offer_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job/job_offer_detail.html")

    def test_job_offer_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)   
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)   

    def test_job_offer_admin_creation(self):
        self.client.login(username='test', password='test')
        nmb = JobOffer.objects.count()
        response = self.client.post(self.url, {"title" : 'title', "status" : 2, "email" :'email@email.fr', "type":'internship','job_response-INITIAL_FORMS':'0','job_response-TOTAL_FORMS':'1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(nmb+1,JobOffer.objects.count())

    def test_job_offer_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.job_offer.get_absolute_url())
        self.assertContains(response,"editable")

    def test_job_offer_creation(self):
        self.assertTrue(isinstance(self.job_offer,JobOffer))
        self.assertEqual(self.job_offer.email,"test@test.fr")
        self.assertEqual(self.job_offer.type,"internship")

    def test_job_offer_retrieval(self):
        self.assertTrue(self.job_offer in JobOffer.objects.all())
        self.assertTrue(self.job_offer in JobOffer.objects.filter(email="test@test.fr"))
        self.assertTrue(self.job_offer in JobOffer.objects.filter(type="internship"))

    def test_job_offer_update(self):
        self.job_offer.email="test@django.fr"
        self.assertEqual(1,JobOffer.objects.filter(email="test@test.fr").count())
        self.assertEqual(0,JobOffer.objects.filter(email="test@django.fr").count())
        self.job_offer.save()
        self.assertEqual(0,JobOffer.objects.filter(email="test@test.fr").count())
        self.assertEqual(1,JobOffer.objects.filter(email="test@django.fr").count())   

class JobResponseTests(TestCase):
    
    def setUp(self):
        super(JobResponseTests, self).setUp()
        app = "organization-job"
        model = "joboffer" 
        self.user = User().objects.create_user(username="user", password='test')
        self.file = SimpleUploadedFile('letter.txt'.encode(), 'content'.encode())
        self.job_offer = JobOffer.objects.create(email = "test@test.fr", type="internship")
        self.job_response = JobResponse.objects.create(first_name = "jean", last_name = "dupont", email="jean@dupont.fr" , message="I want this job", 
        curriculum_vitae = self.file, cover_letter = self.file, job_offer = self.job_offer) 
        self.url = urlresolvers.reverse("admin:%s_%s_change" % (app, model),args=(self.job_offer.id,))

    def test_job_response_fk_deletion(self):
        self.job_offer.delete()
        self.assertTrue(self.job_response in JobResponse.objects.filter(job_offer__isnull=True))

    def test_job_response_not_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/change_form.html")
        self.assertContains(response,"jean@dupont.fr")

    def test_job_response_creation(self):
        self.assertTrue(isinstance(self.job_response,JobResponse))
        self.assertEqual(self.job_response.first_name,"jean")
        self.assertEqual(self.job_response.last_name,"dupont")       
        self.assertEqual(self.job_response.email,"jean@dupont.fr")       
        self.assertEqual(self.job_response.message,"I want this job")
        self.assertEqual(self.job_response.job_offer,self.job_offer)

    def test_job_response_retrieval(self):
        self.assertTrue(self.job_response in JobResponse.objects.all())         
        self.assertTrue(self.job_response in JobResponse.objects.filter(first_name = "jean"))         
        self.assertTrue(self.job_response in JobResponse.objects.filter(last_name = "dupont"))         
        self.assertTrue(self.job_response in JobResponse.objects.filter(email="jean@dupont.fr"))         
        self.assertTrue(self.job_response in JobResponse.objects.filter(message="I want this job"))         
        self.assertTrue(self.job_response in JobResponse.objects.filter(job_offer=self.job_offer))         

    def test_job_response_update(self):
        self.job_response.message="I don't want this job"
        self.assertEqual(1,JobResponse.objects.filter(message="I want this job").count())
        self.assertEqual(0,JobResponse.objects.filter(message="I don't want this job").count())
        self.job_response.save()
        self.assertEqual(0,JobResponse.objects.filter(message="I want this job").count())
        self.assertEqual(1,JobResponse.objects.filter(message="I don't want this job").count())   

    def test_job_response_deletion(self):
        self.job_response.delete()
        self.assertFalse(self.job_response in JobResponse.objects.all())
    
