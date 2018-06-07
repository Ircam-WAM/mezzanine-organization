from django.test.testcases import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
import os
from selenium.webdriver.support.ui import WebDriverWait
import requests

class FrontTest(StaticLiveServerTestCase):

    fixtures = ['event.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.webdriver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        cls.webdriver.implicitly_wait(20)
        cls.url="http://app:8000"

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
        if 'value="en" selected="selected"' in self.webdriver.page_source:
            try:
                self.webdriver.find_element_by_xpath('//*[@id="langSelector"]').click()
            except:
                self.webdriver.find_element_by_xpath('//*[@id="langSelector"]').click()                
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.TAB)
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.ENTER)

    def translate_en(self):
        """
        You've to be on a Mezzo page to call this method
        """
        if 'value="fr" selected="selected"' in self.webdriver.page_source:
            try:
                self.webdriver.find_element_by_xpath('//*[@id="langSelector"]').click()
            except:
                self.webdriver.find_element_by_xpath('//*[@id="langSelector"]').click()                
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.TAB)
            self.webdriver.find_element_by_xpath('//*[@id="langSelector"]/li[2]/a').send_keys(Keys.ENTER)