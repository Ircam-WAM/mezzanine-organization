from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException  
from organization.utils.tests_front import FrontTest
from organization.network.models import Organization,Person,DepartmentPage
from selenium.webdriver.common.keys import Keys
from mezzanine_agenda.models import EventCategory,ExternalShop,EventPrice,Event,Season
from unittest import skip
import requests

class AdminEventTestsSelenium(FrontTest):

    @classmethod
    def setUpClass(cls):
        super(AdminEventTestsSelenium, cls).setUpClass()
    
    @classmethod
    def tearDown(cls):
        super(AdminEventTestsSelenium, cls).tearDownClass()

    @skip ('Unable to submit form, thus event is not created')
    def test_event_creation(self):
        self.webdriver.get(self.url + '/')
        self.log_as_admin()
        self.webdriver.get(self.url + '/admin/mezzanine_agenda/event/')
        self.webdriver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        """
        Filling the needed inputs
        """
        self.webdriver.find_element_by_id('id_title_fr').send_keys('Mon evenement')
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
        #TODO Clicking on button is not submitting form
        r = requests.get(self.url + '/agenda/mon-evenemnt/detail')
        self.assertEqual(r.status_code,200)
        self.logout()

                
    @skip("Work In Progress")
    def test_event_keyword(self):
        self.log_as_admin()
        self.webdriver.get(self.url + '/admin/mezzanine_agenda/event/')
        self.webdriver.find_element_by_xpath('//*[@id="content-main"]/ul/li/a').click()
        self.logout()

class EventEditionSelenium(FrontTest):

    @classmethod
    def setUpClass(cls):
        super(EventEditionSelenium,cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(EventEditionSelenium, cls).tearDownClass()
    
    def test_event_title_edition(self):
        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        if "logout" in self.webdriver.page_source:
            self.logout()
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
        WebDriverWait(self.webdriver,10).until(EC.title_contains("update"))
        """
        Change title in an other language
        """
        self.translate_fr()

        if self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar"]/a[2]').value_of_css_property("display")=='none':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').send_keys(Keys.TAB)
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[2]/div/a').send_keys(Keys.ENTER)
        self.webdriver.find_element_by_class_name('charfield').clear()
        self.webdriver.find_element_by_class_name('charfield').send_keys("event search fr")
        self.webdriver.find_element_by_class_name('charfield').send_keys(Keys.ENTER)
        WebDriverWait(self.webdriver,10).until(EC.title_contains("fr"))
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

    def test_event_date_edition_failure_1(self):
        """
        Trying to insert a start date > end date
        """

        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        if "logout" in self.webdriver.page_source:
            self.logout()
        self.log_as_admin()
        self.translate_en()
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').click()
        Select(self.webdriver.find_element_by_xpath('//*[@id="id_start_0_year"]')).select_by_visible_text('2027')
        Select(self.webdriver.find_element_by_xpath('//*[@id="id_end_0_year"]')).select_by_visible_text('2026')
        self.webdriver.find_element_by_css_selector('.datetimefield').send_keys(Keys.ENTER)
        WebDriverWait(self.webdriver, 3).until(EC.alert_is_present())      
        alert = self.webdriver.switch_to.alert
        alert.accept()
        self.logout()

    def test_event_date_edition_failure_2(self):
        """
        Trying to insert a start date > end date
        """

        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        if "logout" in self.webdriver.page_source:
            self.logout()
        self.log_as_admin()
        self.translate_en()
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').click()
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys("15:60")
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys(Keys.ENTER)
        WebDriverWait(self.webdriver, 3).until(EC.alert_is_present())      
        alert = self.webdriver.switch_to.alert
        alert.accept()
        self.logout()

    @skip("Date edition is always sending bad format alert")
    def test_event_date_edition_(self):
        """
        Trying to insert a start date > end date
        """

        self.webdriver.get(self.url + '/agenda/event-search/detail/')
        if "logout" in self.webdriver.page_source:
            self.logout()
        self.log_as_admin()
        self.translate_en()
        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').click()
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys("15:59")
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys(Keys.ENTER)
        self.translate_fr()
        self.assertTrue('15h59' in self.webdriver.page_source)
        self.translate_en()
        self.assertTrue('3:49 p.m' in self.webdriver.page_source)
        
        """
        Reset date
        """

        if self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').value_of_css_property("visibility")=='hidden':
            self.webdriver.find_element_by_xpath('//*[@id="editable-toolbar-toggle"]').click()
        self.webdriver.find_element_by_xpath('//*[@id="container"]/main/div[1]/div[1]/div[3]/div[1]/div/div/a').click()
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys("17:49")
        self.webdriver.find_elements_by_css_selector('.datetimefield')[0].send_keys(Keys.ENTER)        
        self.logout()

