import unittest
import time
import os

from selenium import webdriver

# PhantomJS has been deprecated.
# Zhimin predicted phantom JS was hype on first edition of Selenium Recipes Book (2012)
# despite many 'test automation expert' claimed 'success' of using phantomJS for test automation.
class PhantomJSTestCase(unittest.TestCase):

    def test_phantomjs(self):
        driver = webdriver.PhantomJS()
        driver.get("http://travel.agileway.net")
        driver.set_window_size(1120, 550)
        self.assertEqual("Agile Travel", driver.title)
        driver.quit

