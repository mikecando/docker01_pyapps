import unittest
import os
import urllib
from selenium import webdriver


class TextFieldTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_enter_text_by_name(self):
        self.driver.find_element_by_name("username").send_keys("agileway")

    def test_enter_text_field_by_id(self):
        self.driver.find_element_by_id("user").send_keys("agileway")

    def test_enter_text_in_password_field(self):
        self.driver.find_element_by_id("pass").send_keys("testisfun")

    def test_enter_text_in_multi_row_textarea(self):
        self.driver.find_element_by_id("comments").send_keys("Automated testing is\nFun!")

    def test_clear_all_text_in_text_field(self):
        self.driver.find_element_by_id("user").send_keys("testwisely")
        self.driver.find_element_by_name("username").clear();

    # Selenium, different from Watir, does not have focus
    # Instead, calling send_keys will focus on th element
    def test_focus_on_text_field(self):
        self.driver.find_element_by_id("pass").send_keys("")

    def test_focus_on_text_field_using_javascript(self):
        elem = self.driver.find_element_by_id("pass")
        self.driver.execute_script("arguments[0].focus();", elem);

    ## Assert
    def test_assert_value_in_textfield(self):
        self.driver.find_element_by_id("user").send_keys("testwisely")
        self.assertEqual(self.driver.find_element_by_id("user").get_attribute("value"), "testwisely")

    # Using JavaScript
    def test_set_value_in_readonly_or_disabled_textfield(self):
        # the below won't work for read_only text fields
        # driver.find_element(:id, "writable").send_keys("new value")
        self.driver.execute_script("$('#readonly_text').val('bypass');")
        self.assertEqual(self.driver.find_element_by_id("readonly_text").get_attribute("value"), "bypass")

        self.driver.execute_script("$('#disabled_text').val('anyuse');")
        self.assertEqual(self.driver.find_element_by_id("disabled_text").get_attribute("value"), "anyuse")

    def test_set_and_asset_hidden_field(self):
        the_hidden_elem = self.driver.find_element_by_name("currency")
        self.assertEqual(the_hidden_elem.get_attribute("value"), "USD")
        self.driver.execute_script("arguments[0].value = 'AUD';", the_hidden_elem)
        self.assertEqual(self.driver.find_element_by_name("currency").get_attribute("value"), "AUD")