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

from django.contrib.auth.admin import UserAdmin
from mezzanine.utils.tests import TestCase
from organization.agenda.models import *
from mezzanine_agenda.models import EventCategory,ExternalShop,EventPrice,Event,Season
from mezzanine_agenda.admin import EventAdmin
import datetime
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED,KeywordsField
from mezzanine.generic.models import Keyword,AssignedKeyword
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.images import ImageFile
import tempfile
from django.contrib.auth import get_user_model as User
from django.core import urlresolvers
from unittest import skip

# Create your tests here.

class URLTests(TestCase):
    
    def setUp(self):
        super(URLTests, self).setUp()
        self.basic_user = User().objects.create_user(username="user", password='test')
        """
        This simulate an event creation on front,
        a keyword is created when keywords field is filled
        """
        keyword = Keyword.objects.create(title="scientific event")
        self.event_tagged = Event.objects.create(title="mon-evenement", start=datetime.date.today() + datetime.timedelta(days=1),user=self.basic_user,keywords_string="scientific event")
        AssignedKeyword.objects.create(keyword_id=keyword.id,content_object=self.event_tagged)
        s1 = Season.objects.create(title="s1",start=datetime.datetime.strptime("2016-06-01", "%Y-%m-%d"),end=datetime.datetime.strptime("2016-05-31", "%Y-%m-%d"))
        s2 = Season.objects.create(title="s2",start=datetime.datetime.strptime("2017-06-01", "%Y-%m-%d"),end=datetime.datetime.strptime("2017-05-31", "%Y-%m-%d"))
        s3 = Season.objects.create(title="s3",start=datetime.datetime.strptime("2018-06-01", "%Y-%m-%d"),end=datetime.datetime.strptime("2018-05-31", "%Y-%m-%d"))
        self.event_archive = Event.objects.create(title="past_event",start=datetime.datetime.strptime("2017-04-02", "%Y-%m-%d"), user=self.basic_user)

    def test_url_tag(self):
        response = self.client.get('/agenda/tag/scientific-event/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"mon-evenement")
        self.assertTemplateUsed(response,'agenda/event_list.html')

    def test_url_archive(self):
        response = self.client.get('/agenda/archive/2017/')
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"past_event")
        response = self.client.get('/agenda/archive/2016/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"past_event")
        self.assertTemplateUsed(response,'agenda/event_list.html')

    def test_url_slug(self):
        response = self.client.get('/agenda/' + self.event_tagged.slug + '/detail/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"mon-evenement")
        self.assertTemplateUsed(response,'agenda/event_detail.html')

    def test_basic_url(self):
        response = self.client.get('/agenda/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"mon-evenement")
        self.assertTemplateUsed(response,'agenda/event_list.html')

    def test_url_booking(self):
        response = self.client.get('/agenda/' + self.event_tagged.slug + '/booking/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"mon-evenement")      
        self.assertTemplateUsed(response,'agenda/event_booking.html')

    def test_url_price_autocomplete(self):
        response = self.client.get('/agenda/event-price-autocomplete')
        self.assertEqual(response.status_code,200)

    def test_url_dynamic_content_event_view(self):
        self.client.logout()
        response = self.client.get('/dynamic-content-event/')
        self.assertEqual(response.status_code,302)
        self.client.login(username='test', password='test')
        response = self.client.get('/dynamic-content-event/')
        self.assertEqual(response.status_code,200)


class EventTests(TestCase):

    def setUp(self):
        super(EventTests, self).setUp()
        app = "mezzanine_agenda"
        model = "event" 
        self.url = urlresolvers.reverse("admin:%s_%s_add" % (app, model))
        self.user = User().objects.create_user(username="user", password='test')
        self.parent_event = Event.objects.create(start = datetime.datetime.today(), title="parent_event", user=self._user)
        self.category = EventCategory.objects.create(name="category")
        self.shop = ExternalShop.objects.create()
        file = tempfile.NamedTemporaryFile(suffix='.png')
        img = ImageFile(file, name=file.name)
        self.event = Event.objects.create(title="mon-evenement", start=datetime.datetime.strptime("2018-01-13", "%Y-%m-%d").date(), end = datetime.datetime.strptime("2018-01-18", "%Y-%m-%d").date(),user=self.user,
        status=CONTENT_STATUS_PUBLISHED, category = self.category, facebook_event = 10, shop = self.shop, external_id= 12, is_full = True,
        brochure = img, no_price_comments="no_price_comments", mentions="mentions", allow_comments=True, rank = 2)
        # self.event = Event.objects.create(title="mon-evenement", start=datetime.strptime("2018-01-13", "%Y-%m-%d").date(), end = datetime.strptime("2018-01-18", "%Y-%m-%d").date(),user=self._user,
        # status=CONTENT_STATUS_PUBLISHED, parent = self.parent_event, category = self.category, facebook_event = 10, shop = self.shop, external_id= 12, is_full = True,
        # brochure = img, no_price_comments="no_price_comments", mentions="mentions", allow_comments=True, rank = 2)

    def test_event_display_for_everyone(self):
        self.client.logout()
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agenda/event_detail.html")
        self.client.login(username='user', password='test')
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agenda/event_detail.html")
        self.client.login(username='test', password='test')
        response = self.client.get(self.event.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "agenda/event_detail.html")
        
    @skip("No translation")
    def test_event_admin(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='user', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)   
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)    
               
    @skip('No translation')
    def test_event_admin_creation(self):
        self.client.login(username='test', password='test')
        response = self.client.post(self.url, {"title" : 'titre', "status" : 2, "user" :1, "start_0" :'30/04/2018'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1,Event.objects.count())

    def test_event_admin_edition(self):
        self.client.logout()
        response = self.client.get(self.event.get_absolute_url())
        self.assertNotContains(response,"editable")
        self.client.login(username='user', password='test')
        response = self.client.get(self.event.get_absolute_url())
        self.assertContains(response,"editable")
        self.client.login(username='test', password='test')
        response = self.client.get(self.event.get_absolute_url())
        self.assertContains(response,"editable")

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
        next_event = Event.objects.create(title="mon-futur-evenement", start=datetime.datetime.strptime("2018-01-14", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        previous_event =  Event.objects.create(title="mon-evenement-passe", start=datetime.datetime.strptime("2018-01-12", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        self.assertEqual(self.event.get_previous_by_start_date(),previous_event)
        self.assertEqual(self.event.get_next_by_start_date(),next_event)

    def test_event_start_end_date(self):
        event = Event(start = datetime.datetime.today(), title="parent_event", user=self._user, end = datetime.datetime.strptime("2018-01-14", "%Y-%m-%d").date())
        self.assertRaises(ValidationError, event.save())

    def test_event_creation(self):
        self.assertTrue(isinstance(self.event,Event))
        self.assertEqual(self.event.title,"mon-evenement")
        self.assertEqual(self.event.start,datetime.datetime.strptime("2018-01-13", "%Y-%m-%d").date())
        self.assertEqual(self.event.end,datetime.datetime.strptime("2018-01-18", "%Y-%m-%d").date())
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
        self.assertTrue(self.event in Event.objects.filter(start=datetime.datetime.strptime("2018-01-13", "%Y-%m-%d").date()))
        self.assertTrue(self.event in Event.objects.filter(end=datetime.datetime.strptime("2018-01-18", "%Y-%m-%d").date()))
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