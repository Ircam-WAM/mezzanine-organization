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
from organization.agenda.models import *
from mezzanine_agenda.models import EventCategory,EventShop,EventPrice

from datetime import datetime
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.images import ImageFile
import tempfile
from django.contrib.auth import get_user_model as User


# Create your tests here.

# Make sure selenium is working : python manage.py test organization.agenda.tests.EventTestsSelenium.test_load_page

class EventTests(TestCase):

    """fixtures = ['/srv/lib/mezzanine-organization/organization/agenda/fixtures/event.json']"""
    
    def setUp(self):
        super(EventTests, self).setUp()
        self.user = User().objects.create()
        self.parent_event = Event.objects.create(start = datetime.today(), title="parent_event", user=self._user)
        self.category = EventCategory.objects.create(name="category")
        self.shop = EventShop.objects.create()
        file = tempfile.NamedTemporaryFile(suffix='.png')
        img = ImageFile(file, name=file.name)
        self.event = Event.objects.create(title="mon-evenement", start=datetime.strptime("2018-01-13", "%Y-%m-%d").date(), end = datetime.strptime("2018-01-18", "%Y-%m-%d").date(),user=self.user,
        status=CONTENT_STATUS_PUBLISHED, category = self.category, facebook_event = 10, shop = self.shop, external_id= 12, is_full = True,
        brochure = img, no_price_comments="no_price_comments", mentions="mentions", allow_comments=True, rank = 2)
        # self.event = Event.objects.create(title="mon-evenement", start=datetime.strptime("2018-01-13", "%Y-%m-%d").date(), end = datetime.strptime("2018-01-18", "%Y-%m-%d").date(),user=self._user,
        # status=CONTENT_STATUS_PUBLISHED, parent = self.parent_event, category = self.category, facebook_event = 10, shop = self.shop, external_id= 12, is_full = True,
        # brochure = img, no_price_comments="no_price_comments", mentions="mentions", allow_comments=True, rank = 2)

    def test_event_display(self):
        self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.event.get_absolute_url(), 200)

    def test_event_many_to_many_fields(self):
        event_price = EventPrice.objects.create(value=1,unit=1)
        self.event.prices.add(event_price)
        self.assertEqual(1,self.event.prices.all().count())
        event_price = EventPrice.objects.create(value=1,unit=1)
        self.event.prices.add(event_price)
        self.assertEqual(2,self.event.prices.all().count())
        event_price = EventPrice.objects.create(value=1,unit=1)
        self.event.prices.add(event_price)
        self.assertEqual(3,self.event.prices.all().count())

    def test_event_previous_next_date(self):
        next_event = Event.objects.create(title="mon-futur-evenement", start=datetime.strptime("2018-01-14", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        previous_event =  Event.objects.create(title="mon-evenement-passe", start=datetime.strptime("2018-01-12", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        self.assertEqual(self.event.get_previous_by_start_date(),previous_event)
        self.assertEqual(self.event.get_next_by_start_date(),next_event)

    def test_event_start_end_date(self):
        event = Event(start = datetime.today(), title="parent_event", user=self._user, end = datetime.strptime("2018-01-14", "%Y-%m-%d").date())
        self.assertRaises(ValidationError, event.save())

    def test_event_creation(self):
        self.assertTrue(isinstance(self.event,Event))
        self.assertEqual(self.event.title,"mon-evenement")
        self.assertEqual(self.event.start,datetime.strptime("2018-01-13", "%Y-%m-%d").date())
        self.assertEqual(self.event.end,datetime.strptime("2018-01-18", "%Y-%m-%d").date())
        self.assertEqual(self.event.user,self.user)
        self.assertEqual(self.event.status,CONTENT_STATUS_PUBLISHED)
        self.assertEqual(self.event.category,self.category)
        self.assertEqual(self.event.facebook_event,10)
        self.assertEqual(self.event.shop,self.shop)
        self.assertEqual(self.event.external_id,12)
        self.assertTrue(self.event.is_full)
        self.assertEqual(self.event.no_price_comments,"no_price_comments")
        self.assertEqual(self.event.mentions,"mentions")
        self.assertTrue(self.event.allow_comments)
        self.assertEqual(self.event.rank,2)

    def test_event_retrieval(self):
        self.assertTrue(self.event in Event.objects.all())
        self.assertTrue(self.event in Event.objects.filter(status=CONTENT_STATUS_PUBLISHED))
        self.assertTrue(self.event in Event.objects.filter(user=self.user))
        self.assertTrue(self.event in Event.objects.filter(start=datetime.strptime("2018-01-13", "%Y-%m-%d").date()))
        self.assertTrue(self.event in Event.objects.filter(end=datetime.strptime("2018-01-18", "%Y-%m-%d").date()))
        self.assertTrue(self.event in Event.objects.filter(category=self.category))
        self.assertTrue(self.event in Event.objects.filter(facebook_event=10))
        self.assertTrue(self.event in Event.objects.filter(shop=self.shop))
        self.assertTrue(self.event in Event.objects.filter(external_id=12))
        self.assertTrue(self.event in Event.objects.filter(is_full=True))
        self.assertTrue(self.event in Event.objects.filter(no_price_comments="no_price_comments"))
        self.assertTrue(self.event in Event.objects.filter(mentions="mentions"))
        self.assertTrue(self.event in Event.objects.filter(allow_comments=True))
        self.assertTrue(self.event in Event.objects.filter(rank=2))     

    def test_event_update(self):
        self.event.title="my-event"
        self.assertEqual(1,Event.objects.filter(title="mon-evenement").count())
        self.assertEqual(0,Event.objects.filter(title="my-event").count())
        self.event.save()
        self.assertEqual(0,Event.objects.filter(title="mon-evenement").count())
        self.assertEqual(1,Event.objects.filter(title="my-event").count())        
    
    def test_event_deletion(self):
        event_block = EventBlock.objects.create(event = self.event)
        event_image = EventImage.objects.create(event = self.event)
        event_departement = EventDepartment.objects.create(event = self.event)
        event_person = EventPerson.objects.create(event = self.event)
        link_type = LinkType.objects.create(name = "test link")
        event_link = EventLink.objects.create(event = self.event,link_type=link_type)
        event_playlist = EventPlaylist.objects.create(event = self.event)
        event_period = EventPeriod.objects.create(event = self.event)
        event_training = EventTraining.objects.create(event = self.event)
        event_related_title = EventRelatedTitle.objects.create(event = self.event)
        event_dynamic_content = DynamicContentEvent.objects.create(event = self.event)
        self.event.delete()
        self.assertTrue(event_block in EventBlock.objects.filter(event__isnull=True))
        self.assertTrue(event_image in EventImage.objects.filter(event__isnull=True))
        self.assertTrue(event_departement in EventDepartment.objects.filter(event__isnull=True))
        self.assertTrue(event_person in EventPerson.objects.filter(event__isnull=True))
        self.assertTrue(event_link in EventLink.objects.filter(event__isnull=True))
        self.assertTrue(event_playlist in EventPlaylist.objects.filter(event__isnull=True))
        self.assertTrue(event_period in EventPeriod.objects.filter(event__isnull=True))
        self.assertTrue(event_training in EventTraining.objects.filter(event__isnull=True))
        self.assertTrue(event_related_title in EventRelatedTitle.objects.filter(event__isnull=True))
        self.assertFalse(event_dynamic_content in DynamicContentEvent.objects.all())
        self.assertFalse(self.event in Event.objects.all())

    def test_event_fk_deletion(self):
        self.parent_event.delete()
        self.category.delete()
        self.shop.delete()
        self.assertTrue(self.event in Event.objects.filter(parent__isnull=True))
        self.assertTrue(self.event in Event.objects.filter(category__isnull=True))
        self.assertTrue(self.event in Event.objects.filter(shop__isnull=True))
        self.user.delete()
        self.assertFalse(self.event in Event.objects.all())