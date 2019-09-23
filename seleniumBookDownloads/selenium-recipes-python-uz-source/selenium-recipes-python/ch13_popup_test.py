import unittest
import time
import os
import urllib
from selenium import webdriver

class PopupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/popup.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_basic_auth_dialog(self):
        self.driver.get("http://tony:password@itest2.com/svn-demo")
        self.driver.find_element_by_link_text("tony/").click()

    def test_modal_dialog(self):
        self.driver.find_element_by_id("bootbox_popup").click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//div[@class='modal-footer']/button[text()='OK']").click()

