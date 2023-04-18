from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class JobTestsSelenium(StaticLiveServerTestCase):

    """fixtures = ['/srv/lib/mezzanine-organization/organization/agenda/fixtures/event.json']"""  # noqa: E501

    @classmethod
    def setUpClass(cls):
        super(JobTestsSelenium, cls).setUpClass()
        cls.selenium = WebDriver().Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(JobTestsSelenium, cls).tearDownClass()
