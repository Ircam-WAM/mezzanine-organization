from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException  
from organization.utils.tests_front import FrontTest
from organization.network.models import Organization,Person,DepartmentPage
from selenium.webdriver.common.keys import Keys
from mezzanine_agenda.models import EventCategory,EventShop,EventPrice,Event,Season

class EventTestsSelenium(FrontTest):

    @classmethod
    def setUpClass(cls):
        super(EventTestsSelenium,cls).setUpClass()
    
    @classmethod
    def tearDown(cls):
        super(EventTestsSelenium, cls).tearDownClass()

    def test_event_creation(self):
        self.log_as_admin()
        self.webdriver.get(self.url + '/admin/mezzanine_agenda/event/')
        self.webdriver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        """
        Filling the needed inputs
        """
        self.webdriver.find_element_by_id('id_title_fr').send_keys('Mon evenement')
        print(self.webdriver.find_element_by_id('id_title_fr').get_attribute('value'))
        self.webdriver.find_element_by_id('id_status_0').click()
        self.webdriver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[8]/div/p[1]/span[1]/a[1]').click()
        self.webdriver.find_element_by_xpath('//*[@id="event_form"]/div/fieldset/div[8]/div/p[1]/span[2]/a[1]').click()
        self.webdriver.find_element_by_id('id_start_0').send_keys('19/04/2018')
        self.webdriver.find_element_by_id('id_start_1').send_keys('10:07:08')
        self.webdriver.find_element_by_id('id_periods-0-date_from_0').send_keys('20/04/2018')
        self.webdriver.find_element_by_id('id_periods-0-date_from_1').send_keys('10:07:08')
        self.webdriver.find_element_by_id('id_periods-0-date_to_0').send_keys('21/04/2021')
        self.webdriver.find_element_by_id('id_periods-0-date_to_1').send_keys('10:07:08')
        Select(self.webdriver.find_element_by_id('id_user')).select_by_visible_text('admin')
        self.webdriver.find_element_by_xpath('//*[@id="event_form"]/div/div[21]/input[1]').send_keys(Keys.TAB)
        self.webdriver.find_element_by_xpath('//*[@id="event_form"]/div/div[21]/input[1]').send_keys(Keys.ENTER)
        #TODO Submit not working yet
        print(self.webdriver.page_source)    
        self.logout()
                
    # def test_event_keyword(self):
    #     self.log_as_admin()
    #     self.webdriver.get(self.url + '/admin/mezzanine_agenda/event/')
    #     self.webdriver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
    #     self.logout()

class EventEditionSelenium(FrontTest):

    @classmethod
    def setUpClass(cls):
        super(EventEditionSelenium,cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(EventEditionSelenium, cls).tearDownClass()

    def test_event_title_edition(self):
        if "logout" in self.webdriver.page_source:
            self.logout()
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.assertFalse(self.webdriver.find_elements(By.XPATH,'//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a'))     
        self.log_as_admin()
        self.translate_en()
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').click()
        """
        Change title
        """
        self.webdriver.find_element_by_class_name('charfield').clear()
        self.webdriver.find_element_by_class_name('charfield').send_keys("event search update")
        self.webdriver.find_element_by_class_name('charfield').send_keys(Keys.ENTER)
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.assertTrue("event search update" in self.webdriver.page_source)        

        """
        Change title in an other language
        """
        self.translate_fr()

        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').click()
        self.webdriver.find_element_by_class_name('charfield').clear()
        self.webdriver.find_element_by_class_name('charfield').send_keys("event search fr")
        self.webdriver.find_element_by_class_name('charfield').send_keys(Keys.ENTER)
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.assertTrue("event search fr" in self.webdriver.page_source)        
        self.assertTrue("event search update" not in self.webdriver.page_source)

        self.translate_en()
        """
        Check if the title is still the same in previous language
        """

        self.assertTrue("event search fr" not in self.webdriver.page_source)        
        self.assertTrue("event search update" in self.webdriver.page_source)    

        """
        Reset data
        """

        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').click()
        self.webdriver.find_element_by_class_name('charfield').clear()
        self.webdriver.find_element_by_class_name('charfield').send_keys("event search")
        self.webdriver.find_element_by_class_name('charfield').send_keys(Keys.ENTER)
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.translate_fr()
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').click()
        self.webdriver.find_element_by_class_name('charfield').clear()
        self.webdriver.find_element_by_class_name('charfield').send_keys("event search")
        self.webdriver.find_element_by_class_name('charfield').send_keys(Keys.ENTER)
        self.logout()

    def test_event_date_edition(self):
        if "logout" in self.webdriver.page_source:
            self.logout()
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.assertFalse(self.webdriver.find_elements(By.XPATH,'//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a'))     
        self.log_as_admin()
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').click()
        """
        Change date
        """
        self.webdriver.find_element_by_name('start_1').clear()
        self.webdriver.find_element_by_name('start_1').send_keys("18:49:49")
        self.webdriver.find_element_by_name('start_1').send_keys(Keys.ENTER)
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        self.assertTrue("18:49" in self.webdriver.page_source)        
        self.logout()


class SearchTestsSelenium(FrontTest):               


    @classmethod
    def setUpClass(cls):
        super(SearchTestsSelenium,cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SearchTestsSelenium, cls).tearDownClass()

    def test_search_event(self):
        self.webdriver.get(self.url + '/')
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('event')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("event search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_department_page(self):    
        self.webdriver.get(self.url + '/')    
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('department')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("department search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_team_page(self):      
        self.webdriver.get(self.url + '/')  
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('team')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("team search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_person(self):        
        self.webdriver.get(self.url + '/')
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('person')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("person search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_custom_page(self):    
        self.webdriver.get(self.url + '/')    
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('custom')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("custom page search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_project_topic_page(self):
        self.webdriver.get(self.url + '/')        
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('project')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("project topic search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_playlist(self):        
        self.webdriver.get(self.url + '/')
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('playlist')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("playlist search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_product(self):        
        self.webdriver.get(self.url + '/')
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('product')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("product search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)

    def test_search_article(self):        
        self.webdriver.get(self.url + '/')
        self.webdriver.find_element_by_xpath('//*[@id="navHeader"]/ul/li[4]/a').click()
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys('article')
        self.webdriver.find_element_by_xpath('//*[@id="search"]/div[2]/div/div/div/div/form/input').send_keys(Keys.ENTER)
        self.assertTrue("article search" in self.webdriver.page_source)
        self.translate_fr()
        self.assertTrue("event search" in self.webdriver.page_source)
