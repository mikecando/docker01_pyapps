import unittest
import time
import os
from selenium import webdriver

class FirefoxPluginTestCase(unittest.TestCase):

    def get_firefox_profile_folder_by_name(self, profile_name):
        if platform.system() == "Darwin":
            FF_PROFILE_PATH = "/Users/zhimin/Library/Application Support/Firefox/Profiles"
        elif platform.system() == "Linux":
            FF_PROFILE_PATH = "/home/zhimin/.mozilla/firefox"
        else:
            FF_PROFILE_PATH = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')

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

    def test_use_firefox_autoauth_plugin_using_function(self):
        print(self.get_firefox_profile_folder_by_name("testing"))
        fp = webdriver.FirefoxProfile(self.get_firefox_profile_folder_by_name("testing"))
        fp.add_extension(os.path.join( os.path.dirname(os.path.realpath(__file__)), 'autoauth-2.1-fx+fn.xpi'))
        # Auto Login inform saved  https://addons.mozilla.org/en-US/firefox/addon/autoauth/
        driver = webdriver.Firefox(fp)
        driver.get("http://itest2.com/svn-demo/")
        driver.find_element_by_link_text("tony/").click()
        time.sleep(3)
        driver.quit()
