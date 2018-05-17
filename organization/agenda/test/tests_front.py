from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException  
from organization.utils.tests_front import FrontTest

class EventTestsSelenium(FrontTest):

    def setUp(self):
        super(EventTestsSelenium,self).setUp()
    
    def tearDown(self):
        super(EventTestsSelenium, self).tearDown()

    def test_event_creation(self):
        self.log_as_admin()
        self.webdriver.get(self.url + '/admin/mezzanine_agenda/event/')
        print(self.webdriver.page_source)
        self.webdriver.find_element_by_link_text('add/').click()
        """
        Filling the needed inputs
        """
        self.webdriver.driver.find_element_by_id('id_title_fr').send_keys('Mon evenement')
        self.webdriver.driver.find_element_by_id('id_status_0').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[6]/div/p/a[1]').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[6]/div/p/a[2]').click()
        Select(self.webdriver.find_element_by_id('id_start_0').send_keys('19/04/2021'))
        self.webdriver.driver.find_element_by_id('id_start_1').send_keys('10:07:08')
        self.webdriver.driver.find_element_by_id('id_periods-0-date_from_0').send_keys('20/04/2021')
        self.webdriver.driver.find_element_by_id('id_periods-0-date_from_1').send_keys('10:07:08')
        self.webdriver.driver.find_element_by_id('id_periods-0-date_to_0').send_keys('21/04/2021')
        self.webdriver.driver.find_element_by_id('id_periods-0-date_to_1').send_keys('10:07:08')
        self.webdriver.driver.find_element_by_xpath("//div[@id='blocks-group']/ul[1]/li[1]/a[1]").click()
        self.webdriver.driver.find_element_by_id('id_blocks-0-content_fr').send_keys("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        """)
        self.webdriver.driver.find_element_by_id('id_blocks-0-title_fr').send_keys("Lorem ipsum")
        Select(self.webdriver.driver.find_element_by_id('id_departments-0-department')).select_by_visible_text('Organisation 1')
        Select(self.webdriver.driver.find_element_by_id('id_persons-0-person')).select_by_visible_text('Personne 1')
        self.webdriver.driver.find_element_by_name('_save').click()
        try:
            self.webdriver.driver.find_element_by_class_name("success")
        except NoSuchElementException:
            return False
        return True

class SearchTestsSelenium(FrontTest):               
    
    def setUp(self):
        super(SearchTestsSelenium,self).setUp()
        self.webdriver.get('%s%s' % (self.live_server_url, '/'))

    def tearDown(self):
        super(SearchTestsSelenium, self).tearDown()

    def test_search_person(self):
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('personne')
        try:
            self.webdriver.driver.find_element_by_link_text( "/person/personne-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_department_page(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('department')
        try:
            self.webdriver.driver.find_element_by_link_text("/page-department-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_team_page(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('team')
        try:
            self.webdriver.driver.find_element_by_link_text("/page-team-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_event(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('ev')
        try:
            self.webdriver.driver.find_element_by_link_text("/agenda/mon-evenement/detail/")
        except NoSuchElementException:
            return False
        return True

    def test_search_custom_page(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('custom')
        try:
            self.webdriver.driver.find_element_by_link_text("/custom-page-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_project_topic_page(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('project')
        try:
            self.webdriver.driver.find_element_by_link_text("/project-page-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_playlist(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('playlist')
        try:
            self.webdriver.driver.find_element_by_link_text("/playlists/playlist1/detail/")
        except NoSuchElementException:
            return False
        return True

    def test_search_product(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('produit')
        try:
            self.webdriver.driver.find_element_by_link_text("shop/product/produit-1/")
        except NoSuchElementException:
            return False
        return True

    def test_search_article(self):        
        self.webdriver.driver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a ').click()
        self.webdriver.driver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('article')
        try:
            self.webdriver.driver.find_element_by_link_text("article/detail/article-1/")
        except NoSuchElementException:
            return False
        return True

       