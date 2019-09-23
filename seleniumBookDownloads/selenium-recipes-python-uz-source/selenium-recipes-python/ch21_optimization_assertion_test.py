import unittest
import time
import random
import os
import os.path
import urllib
import csv
import time
import xlrd  # pip install xlrd, a library for extract data from Excel
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

class OptmizationAssertionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/WebDriverStandard.html")

    @classmethod
    def tearDownClass(cls):
        # print("tear down")
        cls.driver.quit()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_search_text_in_page_source_is_faster_than_page_text(self):
        import time
        start_time = time.time()
        self.assertIn("language-neutral wire protocol", self.driver.find_element_by_tag_name("body").text)
        print("Method 1: Search whole document text took ", time.time() - start_time, " seconds")

        start_time = time.time()
        self.assertIn("language-neutral wire protocol", self.driver.page_source)
        print("Method 2: Search whole document HTML took ", time.time() - start_time, " seconds")

    def test_specific_element_assertion_faster(self):
        start_time = time.time()
        self.assertIn("language-neutral wire protocol", self.driver.find_element_by_tag_name("body").text)
        print("Method 1: Search whole document text took ", time.time() - start_time, " seconds")
        start_time = time.time()
        self.assertIn("language-neutral wire protocol", self.driver.find_element_by_id("abstract").text)
        print("Method 2: Search specific element text took ", time.time() - start_time, " seconds")

    def test_use_cached_page_data(self):
        start_time = time.time()
        self.assertIn("Firefox", self.driver.find_element_by_tag_name("body").text)
        self.assertIn("chrome", self.driver.find_element_by_tag_name("body").text)
        self.assertIn("W3C", self.driver.find_element_by_tag_name("body").text)
        print("Method One: 3 assertions took ", time.time() - start_time, " seconds")

        # a much more efficient way
        start_time = time.time()
        the_page_text = self.driver.find_element_by_tag_name("body").text
        self.assertIn("Firefox", the_page_text)
        self.assertIn("chrome", the_page_text)
        self.assertIn("W3C", the_page_text)
        print("Method Two: 3 assertions took ", time.time() - start_time, " seconds")