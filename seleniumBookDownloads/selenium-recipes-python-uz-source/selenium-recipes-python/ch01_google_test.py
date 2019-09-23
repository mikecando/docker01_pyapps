import unittest
import time
import os
from selenium import webdriver

class GoogleTestCase(unittest.TestCase):

    site_url = "https://google.com"
    
    def test_start_chrome(self):
        driver = webdriver.Chrome()
        driver.get(self.site_url)
        time.sleep(1)
        driver.quit()
        
    def test_start_firefox_and_assert_title(self):
        driver =  webdriver.Firefox()
        driver.get(self.site_url)
        self.assertEqual("Google", driver.title)
        time.sleep(1)
        driver.quit()
        
    def test_start_ie(self):
        if os.name == "nt":
          driver = webdriver.Ie()
          driver.get(self.site_url)
          time.sleep(1)
          driver.quit()
        else:
          print("Non windows platform, skip")

