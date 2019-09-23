import unittest
import time
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

# API http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains

class AdvancedUserInteractionsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file://"  + self.site_url() + "/../site/html5.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path
        
    def test_double_click(self):
        self.driver.get("file://"  + self.site_url() + "/../site/text_field.html")
        elem = self.driver.find_element_by_id("pass")
        ActionChains(self.driver).double_click(elem).perform()

    def test_mouse_over(self):
        elem = self.driver.find_element_by_id("email")
        ActionChains(self.driver).move_to_element(elem).perform()

    def test_click_and_hold_select_multiple_items(self):
        self.driver.get("http://jqueryui.com/selectable")
        self.driver.find_element_by_link_text("Display as grid").click()
        time.sleep(0.5)
        self.driver.switch_to.frame(0)
        list_items = self.driver.find_elements_by_xpath("//ol[@id='selectable']/li")
        ActionChains(self.driver).click_and_hold(list_items[1])\
            .click_and_hold(list_items[3])\
            .click()\
            .perform()
        self.driver.switch_to.default_content()

    def test_right_click(self):
        self.driver.get("file://"  + self.site_url() + "/../site/text_field.html")
        time.sleep(0.5)
        elem = self.driver.find_element_by_id("pass")
        # browser specific, paste text
        if (self.driver.capabilities["browserName"] == "firefox"):
            ActionChains(self.driver).send_keys(Keys.DOWN)\
                .send_keys(Keys.DOWN)\
                .send_keys(Keys.DOWN)\
                .send_keys(Keys.DOWN)\
                .send_keys(Keys.RETURN)\
                .perform()

    def test_key_sequences(self):
        self.driver.get("file://"  + self.site_url() + "/../site/text_field.html")
        self.driver.find_element_by_id("comments").send_keys("Multiple Line\r\n Text")
        elem = self.driver.find_element_by_id("comments")
        ActionChains(self.driver).click(elem)\
            .key_down(Keys.CONTROL)\
            .send_keys("a")\
            .key_up(Keys.CONTROL)\
            .perform()
        # this different from click element, the key is send to browser directly
        ActionChains(self.driver).send_keys(Keys.BACKSPACE).perform()

    # this works OK on Chrome, error on Firefox, IE no effect
    def test_drag_and_drop(self):
        self.driver.get("file://"  + self.site_url() + "/../site/drag_n_drop.html")
        drag_from = self.driver.find_element_by_id("item_1")
        target = self.driver.find_element_by_id("trash")
        ActionChains(self.driver).drag_and_drop(drag_from, target).perform()

    def test_slider(self):
        self.assertEqual(self.driver.find_element_by_id("pass_rate").text, "15%")
        elem = self.driver.find_element_by_id("pass-rate-slider")
        ActionChains(self.driver).drag_and_drop_by_offset(elem, 2, 0).perform() # unable to set specific value
        self.assertNotEqual(self.driver.find_element_by_id("pass_rate").text, "15%")


