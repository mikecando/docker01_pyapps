import unittest
import time
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

class Select2TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("DEBUG")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/select2.html")
        time.sleep(1) # wait enough time to load JS

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_select2_single(self):
        self.driver.find_element_by_xpath("//select[@id='country_single']/../span").click()
        available_items = self.driver.find_elements_by_xpath("//ul[@id='select2-country_single-results']/li")
        for x in available_items:
            if x.text == "Australia":
                x.click()
                break
        time.sleep(1)
        self.driver.find_element_by_xpath("//select[@id='country_single']/../span").click()
        available_items = self.driver.find_elements_by_xpath("//ul[@id='select2-country_single-results']/li")
        for x in available_items:
            if x.text == "United States":
                x.click()
                break

    def test_select2_single_with_search(self):
        # Now search for an option
        time.sleep(1)
        self.driver.find_element_by_xpath("//select[@id='country_single']/../span//span[@class='select2-selection__arrow']").click()

        search_text_field = self.driver.find_element_by_xpath("//span/input[@class = 'select2-search__field']")
        search_text_field.send_keys("United King")
        time.sleep(0.5) # let filtering finishing
        # select first highlighted option
        search_text_field.send_keys(Keys.ENTER)

    def test_select2_multiple(self):
        # click the box then select one option
        select2_multi_container_xpath = "//select[@id='country_multiple']/../span[contains(@class, 'select2-container')]"
        self.driver.find_element_by_xpath(select2_multi_container_xpath).click()
        available_items = self.driver.find_elements_by_xpath("//ul[@id='select2-country_multiple-results']/li")
        for x in available_items:
            if x.text == "Australia":
                x.click()
                break
        time.sleep(0.3)

        # select another
        self.driver.find_element_by_xpath(select2_multi_container_xpath).click()
        available_items = self.driver.find_elements_by_xpath("//ul[@id='select2-country_multiple-results']/li")
        for x in available_items:
            if x.text == "United Kingdom":
                x.click()
                break

        # clear all selections
        time.sleep(0.5)
        close_btns = self.driver.find_elements_by_xpath(select2_multi_container_xpath + "//span[@class='select2-selection__choice__remove']")
        while(len(close_btns) > 0):
            close_btns[0].click();
            time.sleep(0.1)
            close_btns = self.driver.find_elements_by_xpath(select2_multi_container_xpath + "//span[@class='select2-selection__choice__remove']")


    def select2_multiple_clear(self, select_id):
        select2_multi_container_xpath = "//select[@id='" + select_id + "']/../span[contains(@class, 'select2-container')]"
        close_btns = self.driver.find_elements_by_xpath(select2_multi_container_xpath + "//span[@class='select2-selection__choice__remove']")
        flag_cleared = 0
        while (len(close_btns) > 0):
            close_btns[0].click();
            time.sleep(0.1)
            flag_cleared = 1
            close_btns = self.driver.find_elements_by_xpath(select2_multi_container_xpath + "//span[@class='select2-selection__choice__remove']")
        if flag_cleared == 1:
            self.driver.find_element_by_xpath(select2_multi_container_xpath).click()

    def select2_multiple_select(self, select_id, option_label):
        select2_multi_container_xpath = "//select[@id='" + select_id + "']/../span[contains(@class, 'select2-container')]"
        self.driver.find_element_by_xpath(select2_multi_container_xpath).click()
        available_items = self.driver.find_elements_by_xpath("//ul[@id='select2-country_multiple-results']/li")
        for x in available_items:
            if x.text == option_label:
                x.click()
                break

    def test_wrap_chosen_in_reusable_functions(self):
        # ... land to the page with a select2 list
        self.select2_multiple_select("country_multiple", "United States")
        self.select2_multiple_select("country_multiple", "Australia")
        self.select2_multiple_clear("country_multiple")
        self.select2_multiple_select("country_multiple", "United Kingdom")
