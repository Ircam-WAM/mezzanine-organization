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
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from organization.agenda.models import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

# Create your tests here.

# Make sure selenium is working : python manage.py test organization.agenda.tests.EventTestsSelenium.test_load_page

class EventTests(TestCase):

    """fixtures = ['/srv/lib/mezzanine-organization/organization/agenda/fixtures/event.json']"""

    def setUp(self):
        super(EventTests, self).setUp()
        self.event = Event.objects.create(title="mon-evenement", start=datetime.strptime("2018-01-13", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)

    def test_event_display(self):
        self.client.get(self.event.get_absolute_url())
        self.assertEqual(self.event.get_absolute_url(), 200)

    def test_event_date(self):
        next_event = Event.objects.create(title="mon-futur-evenement", start=datetime.strptime("2018-01-14", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        previous_event =  Event.objects.create(title="mon-evenement-passe", start=datetime.strptime("2018-01-12", "%Y-%m-%d").date(), user=self._user, status=CONTENT_STATUS_PUBLISHED)
        self.assertEqual(self.event.get_previous_by_start_date(),previous_event)
        self.assertEqual(self.event.get_next_by_start_date(),next_event)

    def test_event_creation(self):
        self.assertTrue(isinstance(self.event,Event))
        self.assertEqual(self.event.title,"mon-evenement")
        self.assertEqual(self.event.start,datetime.strptime("2018-01-13", "%Y-%m-%d").date())
        self.assertEqual(self.event.user,self._user)

    def test_event_retrieval(self):
        self.assertTrue(self.event in Event.objects.filter(status=CONTENT_STATUS_PUBLISHED))
        self.assertTrue(self.event in Event.objects.all())
        self.assertTrue(self.event in Event.objects.filter(user=self._user))
        self.assertTrue(self.event in Event.objects.filter(start=datetime.strptime("2018-01-13", "%Y-%m-%d").date()))
        self.assertTrue(self.event in Event.objects.filter(user=self._user))

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
        self.assertEqual(0,Event.objects.filter(user=self._user).count())
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

class EventTestsSelenium(StaticLiveServerTestCase):

    fixtures = ['fixtures/event.json']

    @classmethod
    def setUpClass(cls):
        super(EventTestsSelenium,cls).setUpClass()
        cls.selenium = WebDriver().Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(EventTestsSelenium, cls).tearDownClass()

    def test_event_creation(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/mezzanine_agenda/event/'))
        self.selenium.driver.find_element_by_link_text('add/').click()
        """
        Filling the needed inputs
        """
        self.selenium.driver.find_element_by_id('id_title_fr').send_keys('Mon évènement')
        self.selenium.driver.find_element_by_id('id_status_0').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[6]/div/p/a[1]').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[6]/div/p/a[2]').click()
        Select(self.selenium.driver.find_element_by_id('id_user')).select_by_visible_text('admin')
        self.selenium.driver.find_element_by_id('id_start_0').send_keys('19/04/2021')
        self.selenium.driver.find_element_by_id('id_start_1').send_keys('10:07:08')
        self.selenium.driver.find_element_by_id('id_periods-0-date_from_0').send_keys('20/04/2021')
        self.selenium.driver.find_element_by_id('id_periods-0-date_from_1').send_keys('10:07:08')
        self.selenium.driver.find_element_by_id('id_periods-0-date_to_0').send_keys('21/04/2021')
        self.selenium.driver.find_element_by_id('id_periods-0-date_to_1').send_keys('10:07:08')
        self.selenium.driver.find_element_by_xpath("//div[@id='blocks-group']/ul[1]/li[1]/a[1]").click()
        self.selenium.driver.find_element_by_id('id_blocks-0-content_fr').send_keys("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        """)
        self.selenium.driver.find_element_by_id('id_blocks-0-title_fr').send_keys("Lorem ipsum")
        Select(self.selenium.driver.find_element_by_id('id_departments-0-department')).select_by_visible_text('Organisation 1')
        Select(self.selenium.driver.find_element_by_id('id_persons-0-person')).select_by_visible_text('Personne 1')
        self.selenium.driver.find_element_by_name('_save').click()
        try:
            self.selenium.driver.find_element_by_class_name("success")
        except NoSuchElementException:
            return False
        return True


    def test_load_page(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))

class SearchTestsSelenium(StaticLiveServerTestCase):
    """
    Check settings.py
    """

    fixtures = ['/srv/lib/mezzanine-organization/organization/agenda/fixtures/event.json']

    @classmethod
    def setUpClass(cls):
        super(SearchTestsSelenium,cls).setUpClass()
        cls.selenium = WebDriver().Chrome()
        self.selenium.get('%s%s' % (self.live_server_url, '/'))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SearchTestsSelenium, cls).tearDownClass()

    def test_search_person(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('personne')
        try:
            self.selenium.driver.find_element_by_link_text( "/person/personne-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_department_page(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('department')
        try:
            self.selenium.driver.find_element_by_link_text("/page-department-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_team_page(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('team')
        try:
            self.selenium.driver.find_element_by_link_text("/page-team-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_event(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('ev')
        try:
            self.selenium.driver.find_element_by_link_text("/agenda/mon-evenement/detail/")
        except NoSuchElementException:
            return False
        return True

    def test_search_custom_page(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('custom')
        try:
            self.selenium.driver.find_element_by_link_text("/custom-page-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_project_topic_page(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('project')
        try:
            self.selenium.driver.find_element_by_link_text("/project-page-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_playlist(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('playlist')
        try:
            self.selenium.driver.find_element_by_link_text("/playlists/playlist1/detail/")
        except NoSuchElementException:
            return False
        return True

    def test_search_product(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('produit')
        try:
            self.selenium.driver.find_element_by_link_text("shop/product/produit-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_article(self):
        self.selenium.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.selenium.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('article')
        try:
            self.selenium.driver.find_element_by_link_text("article/detail/article-1/")
        except NoSuchElementException:
            return False
        return True
