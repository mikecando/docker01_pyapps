# -*- coding: utf-8 -*-

import unittest
import time
import os
import urllib
from selenium import webdriver

class DebuggingTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/assert.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_print_out_test_in_test_scripts_for_inspection(self):
        print("Now on page: " + self.driver.title)
        app_no = self.driver.find_element_by_id("app_id").text
        print("Application number is " + app_no)


    def test_write_page_or_element_html_to_file_for_inspection(self):      
        file_path = "c:\\temp\\login_page.html" if os.name == "nt" else "/Users/zhimin/tmp/login_page.html" 
        file = open(file_path, "w", encoding='utf-8') # optional unicode
        file.write(self.driver.page_source); # whole page
        file.close()
        the_element = self.driver.find_element_by_id("div_parent")
        the_element_html = self.driver.execute_script("return arguments[0].outerHTML;", the_element)
        file_path = "c:\\temp\\login_parent.xhtml" if os.name == "nt" else "/Users/zhimin/tmp/login_parent.xhtml"         
        f = open(file_path, "w")
        f.write(the_element_html)
        f.close()

    def test_save_screenshot(self):
        file_path = "c:\\temp\\screenshot.png" if os.name == "nt" else "/Users/zhimin/tmp/screenshot.png"       
        self.driver.save_screenshot(file_path)
        # or        
        self.driver.get_screenshot_as_file(file_path)