from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from django.contrib.auth import get_user_model
import os
from django.core.management import call_command
from mezzanine_agenda.models import EventCategory,EventShop,EventPrice,Event,Season
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class FrontTest(LiveServerTestCase):

    os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS']="localhost:8000-8010,8081,9200-9300"
    #call_command('makemigrations','mezzanine_agenda')
    fixtures = ['event.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(Event.objects.all())
        cls.webdriver = webdriver.Remote(command_executor='http://172.17.0.1:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
        cls.url='http://172.17.0.7:8000'
        cls.webdriver.get(cls.url)
        print(cls.webdriver.page_source)
        print(cls.live_server_url)
        cls.live_server_url = 'http://172.17.0.7:8000'
        print(cls.live_server_url)
        print(cls.webdriver.current_url)
        print(os.environ.get(
        'DJANGO_LIVE_TEST_SERVER_ADDRESS'))

    @classmethod
    def tearDownClass(cls):
        cls.webdriver.quit()
        super().tearDownClass()

    def log_as_admin(self):
        curr = self.webdriver.current_url
        self.webdriver.get('%s%s' % (self.url, '/accounts/login/'))
        self.webdriver.find_element_by_id('id_username').send_keys('admin')
        self.webdriver.find_element_by_id('id_password').send_keys('admin')
        self.webdriver.find_element_by_css_selector(".btn.btn-primary.btn-lg.pull-right").click()
        self.webdriver.get(curr)

    def logout(self):
        self.webdriver.get('%s%s' % (self.url, '/accounts/login/'))
        self.webdriver.find_element_by_xpath('//*[@id="ProfilSelector"]/li[1]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="ProfilSelector"]/li[2]/a').click()
        
    def translate_fr(self):
        """
        You've to be on a Mezzo page to call this method
        """
        self.webdriver.get(self.webdriver.current_url)
        if 'value="fr" selected="selected"' not in self.webdriver.page_source:
            self.webdriver.find_elements_by_class_name("lang-switcher__item")[2].click()
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.TAB)
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.ENTER)
            self.webdriver.get(self.webdriver.current_url)

    def translate_en(self):
        """
        You've to be on a Mezzo page to call this method
        """
        self.webdriver.get(self.webdriver.current_url)
        if 'value="fr" selected="selected"' in self.webdriver.page_source:
            self.webdriver.find_elements_by_class_name("lang-switcher__item")[2].click()
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.TAB)
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.ENTER)
            self.webdriver.get(self.webdriver.current_url)
