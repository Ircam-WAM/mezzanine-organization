from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NetworkTestsSelenium(StaticLiveServerTestCase):
    
    """fixtures = ['/srv/lib/mezzanine-organization/organization/agenda/fixtures/event.json']"""

    @classmethod
    def setUpClass(cls):
        super(NetworkTestsSelenium,cls).setUpClass()
        cls.selenium = WebDriver().Chrome()
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(NetworkTestsSelenium, cls).tearDownClass()