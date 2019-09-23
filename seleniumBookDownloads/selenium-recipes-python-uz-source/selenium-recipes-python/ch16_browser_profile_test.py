import unittest
import time
import os

from selenium import webdriver

class BrowserProfileTestCase(unittest.TestCase):


    def test_get_browser_type_and_version(self):
        driver = webdriver.Chrome()
        print(driver.capabilities["browserName"]) # => chrome
        print(driver.capabilities["platform"]) # => Windows NT
        print(driver.capabilities["version"]) # => 70.0.3538.77
        driver.quit()

        driver = webdriver.Firefox()
        self.assertEqual("firefox", driver.capabilities["browserName"])
        print(os.name)
        if os.name == "Darwin":
            self.assertEqual("darwin", driver.capabilities["platform"]) # Mac
        elif os.name == "nt":
            # old versions return :winnt
            self.assertEqual(driver.capabilities["platform"], "WINDOWS")
        print(driver.capabilities["browserVersion"]) # => 22.0
        driver.quit()

        if os.name == "nt":
          driver = webdriver.Ie()
          print(driver.capabilities["browserName"])	# "internet explorer"
          driver.quit()

    def test_go_pass_basic_authentication_by_embedding_user_and_password_in_url(self):
        driver = webdriver.Firefox()
        driver.get("http://tony:password@itest2.com/svn-demo/")
        driver.find_element_by_link_text("tony/").click()
        time.sleep(1)
        driver.quit()

    def test_chrome_download_path(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" :   "C:\TEMP" if os.name == "nt" else "/Users/zhimin/tmp" }
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get("http://zhimin.com/books/pwta")
        driver.find_element_by_link_text("Download").click()
        time.sleep(15) # wait download to complete
        if os.name == "nt":
            self.assertTrue( os.path.isfile("c:/TEMP/practical-web-test-automation-sample.pdf") )
        else:
            self.assertTrue( os.path.isfile("/Users/zhimin/tmp/practical-web-test-automation-sample.pdf") )
        driver.quit()


    # List of profile : http://src.chromium.org/svn/trunk/src/chrome/common/pref_names.cc
    def test_firefox_profile_download_path(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.dir", "C:\TEMP" if os.name == "nt" else "/Users/zhimin/tmp")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf')
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        # disable Firefox's built-in PDF viewer
        fp.set_preference("pdfjs.disabled", True)

        driver = webdriver.Firefox(fp)
        driver.get("http://zhimin.com/books/selenium-recipes")
        driver.find_element_by_link_text("Download").click()
        time.sleep(10 )# wait download to complete
        if os.name == "nt":
            self.assertTrue( os.path.isfile("c:/TEMP/selenium-recipes-in-ruby-sample.pdf") )
        else:
            self.assertTrue( os.path.isfile("/Users/zhimin/tmp/selenium-recipes-in-ruby-sample.pdf") )
        driver.quit()

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


    # more info: http://selenium-python.readthedocs.io/navigating.html#cookies
    def test_cookies(self):
        driver = webdriver.Firefox()
        driver.get("http://travel.agileway.net")
        cookie = { 'name' : 'foo', 'value' : 'bar'}
        driver.add_cookie(cookie)
        cookies_list = driver.get_cookies()
        print(cookies_list.__class__) # <class 'list'>
        retrieved_cookie = driver.get_cookie("foo")
        self.assertEqual("bar", retrieved_cookie["value"])

    def test_responsive_web_pages_by_checking_control_with(self):
        driver = webdriver.Chrome()
        driver.set_window_size(1024, 768)  # Desktop
        driver.get("http://agileway.net")
        width_desktop = driver.find_element_by_name("email").size["width"]
        print(width_desktop)
        driver.set_window_size(768, 1024)  # iPad
        width_ipad = driver.find_element_by_name("email").size["width"]
        print(width_ipad)
        self.assertTrue(width_desktop < width_ipad)  # 358 vs 1050
