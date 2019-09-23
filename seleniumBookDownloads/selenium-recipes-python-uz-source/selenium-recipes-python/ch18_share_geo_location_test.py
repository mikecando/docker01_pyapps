import unittest
import time
import random
import os
import platform
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

# type about:profiles in browser search, to create a new profile 'testing'
def get_firefox_profile_folder_by_name(profile_name):

    if platform.system() == "Darwin":
      FF_PROFILE_PATH = "/Users/zhimin/Library/Application Support/Firefox/Profiles"
    elif platform.system() == "Linux":
     FF_PROFILE_PATH = "/home/zhimin/.mozilla/firefox"
    else:
     FF_PROFILE_PATH = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')

    print(FF_PROFILE_PATH)
    # profile dir will digest.name such as i0rdlto9.testing
    try:
        profiles = os.listdir(FF_PROFILE_PATH)
    except WindowsError:
        print("Could not find profiles directory.")
        raise

    loc = None
    try:
        for dir in profiles:
            if dir.endswith(profile_name):
                loc = dir
                break
    except StopIteration:
        print("Firefox profile not found.")
        raise

    profile_path = os.path.join(FF_PROFILE_PATH, loc)
    return profile_path


class ShareGeoLocationTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        fp = webdriver.FirefoxProfile(get_firefox_profile_folder_by_name("testing"))
        cls.driver = webdriver.Firefox(fp)

    @classmethod
    def tearDownClass(cls):
        print("OK")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("https://testwisely.com/demo/geo-location")

    def test_share_geo_location(self):
        self.driver.find_element_by_id("use_current_location_btn").click()
        time.sleep(3)
        try:
          self.assertIn("Latitude:", self.driver.find_element_by_id("demo").text)
        except:
          print("need to in browser profile set permission to share location ")

    def test_fake_geo_location(self):
        lati   = "-34.915379"  # set geo location for user
        longti = "138.576777"
        self.driver.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){; "
                                   " var position = {'coords' : {'latitude': '" + lati + "','longitude': '" + longti + "'}}; " +
                                   " success(position);}")
        self.driver.find_element_by_id("use_current_location_btn").click()
        time.sleep(1)
        self.assertIn("-34.915379", self.driver.find_element_by_id("demo").text)


