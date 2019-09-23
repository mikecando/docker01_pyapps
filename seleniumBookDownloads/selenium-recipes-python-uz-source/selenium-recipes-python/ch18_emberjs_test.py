import unittest
import time
import random
import os
import urllib

from selenium import webdriver

class EmberJSTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file://" +  self.site_url() + "/../site/emberjs-crud-rest/index.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_emberjs_todo(self):
        self.driver.find_element_by_link_text("Locations").click()
        self.driver.find_element_by_link_text("New location").click()

        ember_text_fields = self.driver.find_elements_by_xpath("//div[@class='controls']/input[@class='ember-view ember-text-field']")
        ember_text_fields[0].send_keys("-24.0034583945")
        ember_text_fields[1].send_keys("146.903459345")
        ember_text_fields[2].send_keys("90%")

        self.driver.find_element_by_xpath( "//button[text() ='Update record']").click()