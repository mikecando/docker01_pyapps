import unittest
import time
import os
import urllib
from selenium import webdriver

class RadioButtonRecipeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/radio_button.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_select_radio_button_by_name_and_value(self):
        self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//input[@name='gender' and @value='male']").click()

    def test_select_radio_button_by_id(self):
        self.driver.find_element_by_id("radio_female").click()
        self.driver.find_element_by_id("radio_female").click() # already selected, no effect

    def test_clear_radio_button_by_name_and_value(self):
        self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").click()
        try:
            self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").clear()
        except:
            # Selenium does not allow
            print("Selenium does not allow clear currently selected radio button, just select another one")
            self.driver.find_element_by_xpath("//input[@name='gender' and @value='male']").click()

    def test_verify_radio_button_is_selected(self):
        self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").click()
        self.assertTrue(self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").is_selected())
        self.assertFalse(self.driver.find_element_by_xpath("//input[@name='gender' and @value='male']").is_selected())

    # General using programming
    def test_find_all_buttons_in_a_radio_group_and_iterate_through_them(self):
        self.assertEqual(len(self.driver.find_elements_by_name("gender")), 2)
        for rb in self.driver.find_elements_by_name("gender"):
            if rb.get_attribute("value") == "female":
                rb.click()

    def test_click_nth_radio_button(self):
        self.driver.find_elements_by_name("gender")[1].click()
        self.assertTrue(self.driver.find_element_by_xpath("//input[@name='gender' and @value='female']").is_selected())
        self.driver.find_elements_by_name("gender")[0].click()
        self.assertTrue(self.driver.find_element_by_xpath("//input[@name='gender' and @value='male']").is_selected())

    def test_click_radio_button_by_the_following_label(self):
        elem = self.driver.find_element_by_xpath("//div[@id='q1']//label[contains(.,'Yes')]/../input[@type='radio']")
        elem.click()

    def test_customize_icheck_radios(self):
        # Error: Element is not clickable
        # self.driver.find_element_by_id("q2_1").click
        self.driver.find_elements_by_class_name("iradio_square-red")[0].click()
        self.driver.find_elements_by_class_name("iradio_square-red")[1].click()

        # More precise with XPath
        self.driver.find_element_by_xpath("//div[contains(@class, 'iradio_square-red')]/input[@type='radio' and @value='male']/..").click()
