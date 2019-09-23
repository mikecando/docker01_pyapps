import unittest
import time
import random
import os
import os.path
import urllib
import csv
import time
import xlrd  # pip install xlrd, a library for extract data from Excel
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

class OptmizationDynamicTestCase(unittest.TestCase):


    # Fixed way
    TARGET_SITE_URL = "https://physio.clinicwise.net"
    # TARGET_SITE_URL = "https://yake.clinicwise.net"
    TARGET_BROWSER = "chrome"
    # TARGET_BROWSER = "firefox"

    def setUp(self):
        natalie_logins =  { "english": "natalie", "french": "dupont", "chinese": "hongyu"}
        mark_logins = { "english": "mark", "french": "marc", "chinese": "li"}
        self.user_lookups = {
            'natalie': natalie_logins,
            'mark':  mark_logins
        }

    def tearDown(self):
        print("tear down")
        self.driver.quit()

    def test_change_browser_or_url_by_updating_constants(self):
        if self.TARGET_BROWSER == "chrome":
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()
        self.driver.get(self.TARGET_SITE_URL)

    def test_use_environment_varaible_to_change_test_behaviour_dynamically(self):
        import os
        site_url = os.environ.get("TARGET_SITE_URL", "https://physio.clinicwise.net")
        browser = os.environ.get("BROWSER", "chrome")
        if browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.driver.get(site_url)

    def test_two_languages(self):
        self.driver = webdriver.Chrome()
        site_url = os.environ.get("TARGET_SITE_URL", "https://physio.clinicwise.net")
        self.driver.get(site_url)
        if "physio" in site_url :
          self.driver.find_element_by_id("username").send_keys("natalie")
          self.driver.find_element_by_id("password").send_keys("test")
          self.driver.find_element_by_id("signin_button").click()
          self.assertIn("Signed in successfully.", self.driver.page_source)
        else:
          self.driver.find_element_by_id("username").send_keys("tuo")
          self.driver.find_element_by_id("password").send_keys("test")
          self.driver.find_element_by_id("signin_button").click()
          self.assertIn("成功登录", self.driver.page_source)

    def is_chinese(self):
        return "yake" in self.site_url

    def test_two_languages_with_tenary_operator(self):
        self.driver = webdriver.Chrome()
        self.site_url = os.environ.get("TARGET_SITE_URL", "https://physio.clinicwise.net")
        self.driver.get(self.site_url)
        self.driver.find_element_by_id("username").send_keys("tuo" if self.is_chinese() else "natalie")
        self.driver.find_element_by_id("password").send_keys("test")
        self.driver.find_element_by_id("signin_button").click()
        self.assertIn("成功登录" if self.is_chinese() else "Signed in successfully.", self.driver.page_source)

    # return the current language used on the site
    def site_lang(self):
        # ... may use self.site_url to determine
        if "yake" in self.site_url:
            return "chinese"
        elif "dentaire" in self.site_url:
            return "french"
        else:
            return "english"

    def test_multiple_languages_1(self):
        self.driver = webdriver.Chrome()
        self.site_url = os.environ.get("TARGET_SITE_URL", "https://physio.clinicwise.net")
        self.driver.get(self.site_url)

        # return the current language used on the site
        if self.site_lang() == "chinese":
          self.driver.find_element_by_id("username").send_keys("hongyu")
        elif self.site_lang() == "french":
          self.driver.find_element_by_id("username").send_keys("dupont")
        else:  # default to english
          self.driver.find_element_by_id("username").send_keys("natalie")

    def user_lookup_1(self, username):
        if self.site_lang() == "chinese":
            return "hongyu"
        elif self.site_lang() == "french":
            return "dupont"
        else:
            return "natalie"

    def user_lookup(self, username):
        return self.user_lookups[username][self.site_lang()]

    def test_multiple_lanaguages_with_user_lookup(self):
        self.driver = webdriver.Chrome()
        self.site_url = os.environ.get("TARGET_SITE_URL", "https://physio.clinicwise.net")
        self.driver.get(self.site_url)
        self.driver.find_element_by_id("username").send_keys(self.user_lookup("natalie"))
        self.driver.find_element_by_id("password").send_keys("test")
        self.driver.find_element_by_id("signin_button").click()
