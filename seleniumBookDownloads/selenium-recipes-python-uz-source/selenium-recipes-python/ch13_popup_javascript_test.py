import unittest
import time
import os
import urllib
from selenium import webdriver
import errno
import os
import signal


class PopupJavaScriptTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/popup.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_file_upload(self):
        selected_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), "testdata", "users.csv")
        # print(selected_file)
        self.driver.find_element_by_name("document[file]").send_keys(selected_file)

    def test_javascript_popup_with_alert_api(self):
        self.driver.get("http://testwisely.com/demo/popups")
        self.driver.find_element_by_xpath("//input[contains(@value, 'Buy Now')]").click()
        a = self.driver.switch_to.alert
        print(a.text)
        if a.text == 'Are you sure?':
            a.accept()
        else:
            a.dismiss()

    def test_javascript_popup_with_javascript(self):
        self.driver.get("http://testwisely.com/demo/popups")
        self.driver.execute_script("window.confirm = function() { return true; }")
        self.driver.execute_script("window.alert = function() { return true; }")
        self.driver.execute_script("window.prompt = function() { return true; }")
        self.driver.find_element_by_id("buy_now_btn").click()

'''
    def test_timeout(self):
        with Timeout(3):
            self.driver.get("http://testwisely.com/demo/popups")
            self.driver.find_element_by_xpath("//input[contains(@value, 'Buy Now')]").click()
        print("wait 3 seconds")
'''