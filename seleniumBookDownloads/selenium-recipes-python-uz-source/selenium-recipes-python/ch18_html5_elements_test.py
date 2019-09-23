import unittest
import time
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

class HTMLElementsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/html5.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_invoke_onclick_event(self):
        self.driver.get("file:" + self.site_url() + "/select_list.html")
        self.driver.find_element_by_name("person_name").clear()
        self.driver.find_element_by_name("person_name").send_keys("Wise Tester")
        self.driver.find_element_by_name("person_name").click()
        self.assertEqual(self.driver.find_element_by_id("tip").text, "Max 20 characters")

    def test_invoke_on_change_event(self):
        self.driver.get("file:" + self.site_url() + "/select_list.html")
        self.driver.find_element_by_name("person_name").clear()
        self.driver.find_element_by_name("person_name").send_keys("Test Wise")
        # another way
        # driver.execute_script("return document.getElementById('person_name_textbox').fireEvent('OnChange')");
        self.driver.execute_script("$('#person_name_textbox').trigger('change')");
        self.assertEqual(self.driver.find_element_by_id("person_name_label").text, "Test Wise")

    def test_email_field(self):
        self.driver.find_element_by_id("email").send_keys("test@wisely.com")

    def test_time_field(self):
        self.driver.find_element_by_id( "start_time_1").send_keys("12:05AM")
        # focus on another ...
        self.driver.find_element_by_id( "home_link").send_keys("")
        time.sleep(0.5)

        # now back to change it
        self.driver.find_element_by_id( "start_time_1").click
        self.driver.find_element_by_id( "start_time_1").send_keys([Keys.DELETE, Keys.LEFT, Keys.DELETE, Keys.LEFT, Keys.DELETE])

        self.driver.find_element_by_id( "start_time_1").send_keys("08")
        time.sleep(0.3)
        self.driver.find_element_by_id( "start_time_1").send_keys("27")
        time.sleep(0.3)
        self.driver.find_element_by_id( "start_time_1").send_keys("AM")
