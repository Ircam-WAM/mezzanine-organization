from organization.utils.tests_front import FrontTest
from selenium.webdriver.common.keys import Keys
import requests


class SearchTestsSelenium(FrontTest):

    @classmethod
    def setUpClass(cls):
        super(SearchTestsSelenium, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SearchTestsSelenium, cls).tearDownClass()

    def _start_search(self, input_search, expected):
        self.webdriver.get(self.url + '/')
        self.translate_fr()
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath(
            '//*[@id="search"]/div[2]/div/div/div/div/form/input'
        ).send_keys(input_search)
        self.webdriver.find_element_by_xpath(
            '//*[@id="search"]/div[2]/div/div/div/div/form/input'
        ).send_keys(Keys.ENTER)
        self.assertTrue(expected in self.webdriver.page_source)

    def _search_multi_languages(self, input_search, expected):
        self._start_search(input_search, expected)
        self.translate_en()
        self.assertTrue(expected in self.webdriver.page_source)
        self.webdriver.find_element_by_xpath(
            '//*[@id="container"]/main/div/div/div[2]/div[2]/div/div/a'
        ).click()
        r = requests.get(self.webdriver.current_url)
        self.assertEqual(r.status_code, 200)

    def _search(self, input_search, expected):
        self._start_search(input_search, expected)
        self.webdriver.find_element_by_xpath(
            '//*[@id="container"]/main/div/div/div[2]/div[2]/div/div/a'
        ).click()
        r = requests.get(self.webdriver.current_url)
        self.assertEqual(r.status_code, 200)

    def test_search_event(self):
        self._search_multi_languages('event', 'event search')

    def test_search_department_page(self):
        self._search('department', 'department search')

    def test_search_team_page(self):
        self._search('team', 'team search')

    def test_search_person(self):
        self._search_multi_languages('person', 'person search')

    def test_search_custom_page(self):
        self._search('custom', 'custom page search')

    def test_search_project_topic_page(self):
        self._search('topic', 'project topic search')

    def test_search_playlist(self):
        self._search('playlist', 'playlist search')

    def test_search_product(self):
        self._search('product', 'product search')

    def test_search_article(self):
        self._search('article', 'article search')
