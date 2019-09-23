import unittest
import time
import os
import urllib
from selenium import webdriver

class LocatorRecipeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("DEBUG")
        cls.driver.quit()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path 
        # return urllib.request.pathname2url(site_path)

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/locators.html")

    def test_by_id(self):
        self.driver.find_element_by_id("submit_btn").click()

    def test_by_name(self):
        self.driver.find_element_by_name("comment").send_keys("Selenium Cool")

    def test_by_link_text(self):
        self.driver.find_element_by_link_text("Cancel").click()

    def test_by_partial_link_text(self):
        # will click the "Cancel" link
        self.driver.find_element_by_partial_link_text("ance").click()

    def test_by_xpath(self):
        self.driver.find_element_by_xpath("//*[@id='div2']/input[@type='checkbox']").click()

    def test_by_tag(self):
        self.assertIn("Selenium Locators", self.driver.find_element_by_tag_name("body").text)

    def test_by_class(self):
        self.driver.find_element_by_class_name("btn-primary").click()
        time.sleep(1)
        self.driver.find_element_by_class_name("btn").click()
        # the below will return error "Compound class names not permitted"
        # self.driver.find_element_by_class_name("btn btn-deault btn-primary").click(

    def test_by_css_selector(self):
        self.driver.find_element_by_css_selector("#div2 > input[type='checkbox']").click()

    def test_chain_find_element_to_find_child_elements(self):
        self.driver.find_element_by_id("div2").find_element_by_name("same").click()

    def test_find_multiple_elements(self):
        checkbox_elems = self.driver.find_elements_by_xpath("//div[@id='container']//input[@type='checkbox']")
        print(len(checkbox_elems))  # => 2
        checkbox_elems[1].click()
