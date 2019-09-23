import unittest
import time
import os
import urllib
from selenium import webdriver

class PopupIETestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Ie()

    @classmethod
    def tearDownClass(cls):
        print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/popup.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return urllib.request.pathname2url(site_path)

    # need to turn on Allow
    def test_ie_modal_dialog(self):
        time.sleep(3)
        self.driver.find_element_by_link_text("Show Modal Dialog").click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1]) # switch to the modal win
        self.driver.find_element_by_name("user").send_keys("in_modal")
        self.driver.switch_to.window(self.driver.window_handles[0]) # switch to the main win
        self.driver.find_element_by_name("status").send_keys("done")
