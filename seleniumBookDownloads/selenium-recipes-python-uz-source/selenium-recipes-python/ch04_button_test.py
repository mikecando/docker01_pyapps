import unittest
import time
import os
import urllib
from selenium import webdriver

class ButtonRecipeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file://"  + self.site_url() + "/../site/button.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_click_button_by_text(self):
        self.driver.find_element_by_xpath("//button[contains(text(),'Choose Selenium')]").click()

    def test_click_form_button_by_text(self):
        # the below will fail, as value contains space characters
        # driver.find_element(:xpath, "//input[@value='Space After']").click
        self.driver.find_element_by_xpath("//input[@value='Space After ']").click()

    def test_submit_form(self):
        elem = self.driver.find_element_by_name("user")
        elem.submit()

    def test_click_button_by_id(self):
        # <button id="choose_selenium_btn" class="nav" data-id="123" style="font-size: 14px;">Choose Selenium</button><
        self.driver.find_element_by_id("choose_selenium_btn").click()

    def test_click_button_by_name(self):
        # <input type="submit" name="submit_action" value="Submit">
        self.driver.find_element_by_name("submit_action").click()


    # Unique to Selenium
    def test_submit_form_by_calling_submit_on_a_form_element(self):
        text_field = self.driver.find_element_by_name("user")
        text_field.submit()

    def test_click_image_button(self):
        # <input type="image" src="images/button_go.gif">
        self.driver.find_element_by_xpath("//input[contains(@src, 'button_go.jpg')]").click()

    def test_click_button_with_javascript(self):
        the_btn = self.driver.find_element_by_id("searchBtn")
        self.driver.execute_script("arguments[0].click();", the_btn);

    def test_verify_displayed_or_hidden(self):
        self.assertTrue(self.driver.find_element_by_id("choose_selenium_btn").is_displayed())
        self.driver.find_element_by_link_text("Hide").click()
        # Warning: .click does not return error, but no effect
        time.sleep(0.5)
        print(self.driver.find_element_by_id("choose_selenium_btn").is_displayed())
        self.assertFalse(self.driver.find_element_by_id("choose_selenium_btn").is_displayed())
        self.driver.find_element_by_link_text("Show").click()
        time.sleep(0.5)
        print(self.driver.find_element_by_id("choose_selenium_btn").is_displayed())
        self.assertTrue(self.driver.find_element_by_id("choose_selenium_btn").is_displayed())

    def test_verify_link_enabled_or_disabled(self):
        self.assertTrue(self.driver.find_element_by_id("choose_selenium_btn").is_enabled())
        self.driver.find_element_by_link_text("Disable").click()
        time.sleep(0.5)
        self.assertFalse(self.driver.find_element_by_id("choose_selenium_btn").is_enabled())
        self.driver.find_element_by_link_text("Enable").click()
        time.sleep(0.5)
        self.assertTrue(self.driver.find_element_by_id("choose_selenium_btn").is_enabled())

# unittest.main()

