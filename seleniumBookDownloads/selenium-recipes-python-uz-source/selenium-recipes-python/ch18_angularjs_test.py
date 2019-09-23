import unittest
import time
import random
import os
import urllib
from selenium import webdriver

class AngularJSTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/angular_todo.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_angularjs_todo(self):
        self.assertIn("1 of 2 remaining", self.driver.page_source)
        self.driver.find_element_by_xpath("//input[@ng-model='todoText']").send_keys("Learn test automation")
        self.driver.find_element_by_xpath("//input[@type = 'submit' and @value='add']").click()
        time.sleep(0.5)
        self.driver.find_elements_by_xpath("//input[@type = 'checkbox' and @ng-model='todo.done']")[2].click()
        time.sleep(1)
        self.assertIn("1 of 3 remaining", self.driver.page_source)