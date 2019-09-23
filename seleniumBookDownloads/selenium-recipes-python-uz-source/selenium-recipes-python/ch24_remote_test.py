import unittest
import time
import random
import os
import os.path
import urllib
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

class RemoteTestCase(unittest.TestCase):

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return urllib.request.pathname2url(site_path)

    def test_remote_driver_firefox(self):
        # needs Selenium Standalone Server (java) running
        driver = webdriver.Remote(desired_capabilities={
            "browserName": "firefox",
        })
        driver.get("http://travel.agileway.net")
        driver.quit()

    def test_remote_driver_chrome(self):
        # needs Selenium Standalone Server (java) running
        driver = webdriver.Remote(
            command_executor = 'http://127.0.0.1:4444/wd/hub',
            desired_capabilities = { "browserName": "chrome" }
        )
        driver.get("http://travel.agileway.net")
        driver.quit()
