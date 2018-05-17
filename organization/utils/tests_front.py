from mezzanine.utils.tests import TestCase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from django.contrib.auth import get_user_model
import os
from selenium.webdriver.common.by import By

class FrontTest(TestCase):
    
    def setUp(self):
        super(FrontTest,self).setUp()
        self.webdriver = webdriver.Remote(command_executor='http://172.17.0.3:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
        self.url='http://172.17.0.4:8000'

    def tearDown(self):
        self.webdriver.quit()
        super(FrontTest, self).tearDown()

    def log_as_admin(self):
        self.webdriver.get('%s%s' % (self.url, '/accounts/login/'))
        self.webdriver.find_element_by_id('id_username').send_keys('admin')
        self.webdriver.find_element_by_id('id_password').send_keys('admin')
        self.webdriver.find_element_by_css_selector(".btn.btn-primary.btn-lg.pull-right").click()