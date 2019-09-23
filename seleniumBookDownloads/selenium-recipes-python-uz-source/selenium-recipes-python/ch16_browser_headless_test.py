import unittest
import time
import os

from selenium import webdriver

class BrowserProfileHeaslessTestCase(unittest.TestCase):

    def test_headless_chrome(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("headless")
        # for some chrome builds, may need switch "--disable-gpu"to avoid errors
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get("http://travel.agileway.net")
        self.assertEqual("Agile Travel", driver.title)
        driver.quit()

    def test_headless_firefox(self):
        firefoxOptions = webdriver.firefox.options.Options();
        firefoxOptions.headless = True
        driver = webdriver.Firefox(firefox_options=firefoxOptions)
        driver.get("https://whenwise.com")
        self.assertEqual("WhenWise - Booking Quality Services Near You", driver.title)
        driver.quit()
