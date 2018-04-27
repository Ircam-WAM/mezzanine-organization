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
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.

class JobOfferTests(TestCase):

    def setUp(self):
        super(JobOfferTests, self).setUp()
        self.file = SimpleUploadedFile('letter.txt'.encode(), 'content'.encode())
        self.job_offer = JobOffer.objects.create(email = "test@test.fr", type="internship")
        self.job_response = JobResponse.objects.create(first_name = "jean", last_name = "dupont", email="jean@dupont.fr" , message="I want this job", 
        curriculum_vitae = self.file, cover_letter = self.file, job_offer = self.job_offer)

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
        self.file = SimpleUploadedFile('letter.txt'.encode(), 'content'.encode())
        self.job_offer = JobOffer.objects.create(email = "test@test.fr", type="internship")
        self.job_response = JobResponse.objects.create(first_name = "jean", last_name = "dupont", email="jean@dupont.fr" , message="I want this job", 
        curriculum_vitae = self.file, cover_letter = self.file, job_offer = self.job_offer) 

    def test_job_response_fk_deletion(self):
        self.job_offer.delete()
        self.assertTrue(self.job_response in JobResponse.objects.filter(job_offer__isnull=True))

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
    
