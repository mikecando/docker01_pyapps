import unittest
import time
import os
import urllib
from selenium import webdriver

class CheckboxRecipeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/checkbox.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_check_checkbox_by_name(self):
        self.driver.find_element_by_name("vehicle_bike").click()

    def test_check_checkbox_by_id_safe_set(self):
        the_checkbox =  self.driver.find_element_by_id("checkbox_car")
        if not the_checkbox.is_selected():
            the_checkbox.click()

    def test_uncheck_checkbox(self):
        the_checkbox = self.driver.find_element_by_name("vehicle_bike")
        the_checkbox.click()
        # can't use clear, that for text field
        # driver.find_element(:id => "checkbox_bike").clear
        if the_checkbox.is_selected():
            the_checkbox.click()

    # Assertion
    def test_verify_checkbox_is_selected(self):
        the_checkbox = self.driver.find_element_by_name("vehicle_bike")
        if not the_checkbox.is_selected():
            the_checkbox.click()
        self.assertTrue(the_checkbox.is_selected())
        the_checkbox.click()
        self.assertFalse(the_checkbox.is_selected())

    def test_chain_find_element_to_find_child_elements(self):
        self.driver.find_element_by_id("div2").find_element_by_name("same").click()

    def test_customize_icheck_checkboxes(self):
        self.driver.find_elements_by_class_name("icheckbox_square-red")[0].click()
        time.sleep(0.5) # add some delays for JavaScript to execute
        self.driver.find_elements_by_class_name("icheckbox_square-red")[1].click()
        time.sleep(0.5)
        # More precise with XPath
        self.driver.find_element_by_xpath("//div[contains(@class, 'icheckbox_square-red')]/input[@type='checkbox' and @value='Soccer']/..").click()
