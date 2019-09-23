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
from selenium.webdriver.support.ui import Select

class GotchasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/gotchas.html")

    @classmethod
    def tearDownClass(cls):
        # print("tear down")
        cls.driver.quit()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_detect_browser(self):
        browser_name = self.driver.capabilities["browserName"]
        print(browser_name)
        if browser_name == "firefox":
            self.driver
            # firefox specific test statement
        elif browser_name == "chrome":
            self.driver
            # chrome specific test statement
        else:
            raise Exception("unsupported browser: " + browser_name)


    def test_search_text_in_page_source_is_faster_than_page_text(self):
        try:
          Select(self.driver.find_element_by_name("vip")).select_by_visible_text("No")
        except:
          Select(self.driver.find_element_by_xpath("//select[@name='vip']")).select_by_visible_text("No")
