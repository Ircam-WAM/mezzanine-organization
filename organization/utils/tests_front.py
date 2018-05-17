from mezzanine.utils.tests import TestCase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from django.contrib.auth import get_user_model
import os
from settings import HUB

class FrontTest(TestCase):
    
    def setUp(self):
        super(FrontTest,self).setUp()
        self.webdriver = webdriver.Remote(command_executor='http://172.17.0.2:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
        self.live_server_url = os.environ.get("APP")
        print(HUB)
        print(HUB)
        print(HUB)
        print(HUB)

    def tearDown(self):
        self.webdriver.quit()
        super(FrontTest, self).tearDown()

    def log_as_admin(self):
        self.webdriver.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        self.selenium.driver.find_element_by_id('id_username').send_keys('test')
        self.selenium.driver.find_element_by_id('id_password').send_keys('test')
        self.selenium.driver.find_element_by_class_name("btn btn-primary btn-lg pull-right").click()