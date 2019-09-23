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

class OptmizationTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")

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
        long_str = "START" + '0' * 1024 * 5  + "END" # just over 5K
        start_time = time.time()
        text_area_elem = self.driver.find_element_by_id("comments")
        text_area_elem.send_keys(long_str)
        print("Method 1: time cost by send_keys:", time.time() - start_time, " seconds")

        start_time = time.time()
        self.driver.execute_script("document.getElementById('comments').value = arguments[0];", long_str)
        print("Method 2: time code JS set", time.time() - start_time, " seconds")

