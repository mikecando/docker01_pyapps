import unittest
import time
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

class ImageMapTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file://"  + self.site_url() + "/../site/image-map.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_click_part_of_image(self):
        self.driver.get("file://"  + self.site_url() + "/../site/image-map.html")
        elem = self.driver.find_element_by_id("agileway_software")
        ActionChains(self.driver).move_to_element_with_offset(elem, 190, 30).click().perform()
        self.assertEqual("ClinicWise - Cloud based Health Clinic Management System", self.driver.title)
        self.driver.get("file://"  + self.site_url() + "/../site/image-map.html")
        elem = self.driver.find_element_by_id("agileway_software")
        ActionChains(self.driver).move_to_element_with_offset(elem, 30, 75).click().perform()
        self.assertEqual("BuildWise - TestWisely", self.driver.title)

   