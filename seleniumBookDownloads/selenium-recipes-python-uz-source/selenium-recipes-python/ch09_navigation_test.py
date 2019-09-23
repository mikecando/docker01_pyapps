import unittest
import time
import os
import urllib
from selenium import webdriver

class NavigationRecipeTestCase(unittest.TestCase):

    site_root_url = "http://testwisely.com"

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("close browser")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/index.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_get_browser_type_and_version(self):
        # capabilities property is a dictionary
        print(self.driver.name) # "firefox", "chrome", "internet explorer"
        print(self.driver.capabilities['version']) #  example: "28.0",  "33.0.1750.152"

    def test_go_to_url(self):
        self.driver.get("https://whenwise.com")

    def test_go_back_forward_and_refresh(self):
        self.driver.find_element_by_link_text("Hyperlink").click()
        self.driver.back()
        self.driver.refresh()
        self.driver.forward()

    def test_resize_browser_window(self):
        self.driver.set_window_size(1024, 768)

    def test_maximize_browser_window(self):
        time.sleep(0.5)
        # NOTE: currently a chromedriver bug https://github.com/SeleniumHQ/docker-selenium/issues/559
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.set_window_size(1024, 768)

    def test_move_browser_window(self):
        self.driver.set_window_position(100, 200)
        time.sleep(1)
        self.driver.set_window_position(0, 0)

    def test_minimze_browser_window(self):
        self.driver.set_window_position(-2000, 0)
        self.driver.find_element_by_link_text("Hyperlink").click()
        time.sleep(2)
        self.driver.set_window_position(0, 0)

    def visit(self, path):
        self.driver.get(self.site_root_url + path)

    def test_go_to_page_within_the_site_using_function(self):
        self.visit("/demo")
        self.visit("/demo/survey")
        self.visit("/") # home page

    def test_remember_one_page_come_back_later(self):
        url = self.driver.current_url
        self.driver.find_element_by_link_text("Button").click()
        # ...
        time.sleep(1)
        self.driver.get(url)

    def test_switch_browser_or_tab(self):
        self.driver.find_element_by_link_text("Hyperlink").click()
        self.driver.find_element_by_link_text("Open new window").click() # target='_blank' link
        self.driver.switch_to.window(self.driver.window_handles[-1]) # switch to the last tab
        self.assertIn("This is url link page", self.driver.find_element_by_tag_name("body").text)
        self.driver.switch_to.window(self.driver.window_handles[0]) # back to first tab
        self.assertTrue(self.driver.find_element_by_link_text("Open new window").is_displayed())

    def test_scroll_to_element(self):
        self.driver.find_element_by_link_text("Button").click()
        self.driver.set_window_size(1024, 200) # make window small
        elem = self.driver.find_element_by_name("submit_action_2")
        elem_pos = elem.location["y"]
        self.driver.execute_script("window.scroll(0, {})".format(elem_pos))
        time.sleep(1)
        elem.click()
        self.driver.set_window_size(1024, 768)

    def test_open_and_close_new_browser_tab(self):
        new_web_page_url = "https://whenwise.com"
        self.driver.execute_script("window.open('" + new_web_page_url + "', '_blank')")
        tab_count = len(self.driver.window_handles)
        self.driver.switch_to.window(self.driver.window_handles[-1]) # switch to the last tab
        time.sleep(1)
        self.driver.find_element_by_link_text("Partner with us").click()
        # now try to close first tab
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_link_text("Hyperlink").click()
        self.driver.close()
        self.assertEqual(tab_count - 1, len(self.driver.window_handles))
        # re-focus
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)
        self.driver.find_element_by_link_text("FREE").click()