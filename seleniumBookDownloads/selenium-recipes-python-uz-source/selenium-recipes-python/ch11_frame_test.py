import unittest
import time
import os
import urllib
from selenium import webdriver

class FrameTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/frames.html")

    def tearDown(self):
        self.driver.switch_to.default_content()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_frames(self):
        self.driver.switch_to.frame("topNav")  # name
        self.driver.find_element_by_link_text("Menu 2 in top frame").click()
        # need to switch to default before another switch
        self.driver.switch_to.default_content()
        # time.sleep(1)
        # self.driver.switch_to.frame("menu") # name
        self.driver.switch_to.frame(self.driver.find_element_by_id("menu_frame"))
        self.driver.find_element_by_link_text("Green Page").click()

        self.driver.switch_to.default_content()
        # for frame in frameset using name or ID
        self.driver.switch_to.frame(self.driver.find_element_by_name("content"))
        self.driver.find_element_by_link_text("Back to original page").click()

    def test_iframe(self):
        self.driver.get("file:" + self.site_url() + "/iframe.html")
        self.driver.find_element_by_name("user").send_keys("agileway")
        self.driver.switch_to.frame("Frame1")
        self.driver.find_element_by_name("username").send_keys("tester")
        self.driver.find_element_by_name("password").send_keys("TestWise")
        self.driver.find_element_by_id("loginBtn").click()
        self.assertIn("Signed in", self.driver.page_source)
        self.driver.switch_to.default_content()
        self.driver.find_element_by_id("accept_terms").click()

    def test_iframe_by_index(self):
        self.driver.get("file:" + self.site_url() + "/iframes.html")
        self.driver.switch_to.frame(0)
        self.driver.find_element_by_name("username").send_keys("agileway")
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)
        self.driver.find_element_by_id("radio_male").click()