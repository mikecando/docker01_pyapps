import unittest
import time
import os
from selenium.common.exceptions import TimeoutException

from selenium import webdriver

class BrowserTimeoutTestCase(unittest.TestCase):

    def setUp(self):
        self.driver =  webdriver.Chrome()

    def tearDown(self):
        self.driver.quit();

    def test_set_max_page_load_time(self):
        try:
          self.driver.set_page_load_timeout(1)  # shall time out
          self.driver.get("https://testwisely.com/demo")
        except TimeoutException as ex:
           print("Browser timed out")

    # WebDriver Ruby normally times out on 60 seconds, Python will keep waiting
    def test_will_not_timeout_slow_page(self):
        self.driver.get("http://travel.agileway.net/delay?delay=65")
