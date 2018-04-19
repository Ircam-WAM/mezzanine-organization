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

# Create your tests here.

# Make sure selenium is working : python manage.py test organization.agenda.tests.EventTestsSelenium.test_load_page

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
        self.selenium.driver.find_element_by_id('id_keywords_1').click()
        self.selenium.driver.find_element_by_id('id_keywords_2').click()
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
            WebDriverWait(self.selenium.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "success"))
            )
        finally:
            self.selenium.driver.quit()

    def test_load_page(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
                  

