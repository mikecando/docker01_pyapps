import unittest
import time
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

class ChosenTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/chosen/index.html")
        time.sleep(1) # wait enough time to load JS

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_chosen_single(self):
        self.driver.find_element_by_xpath("//div[@id='chosen_single_chosen']//a[contains(@class,'chosen-single')]").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='chosen_single_chosen']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == "Australia":
                x.click()
                break
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[@id='chosen_single_chosen']//a[contains(@class,'chosen-single')]").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='chosen_single_chosen']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == "United States":
                x.click()
                break

        # Now search for an option
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[@id='chosen_single_chosen']//a[contains(@class,'chosen-single')]").click()

        search_text_field = self.driver.find_element_by_xpath("//div[@id='chosen_single_chosen']//div[@class='chosen-drop']//div[contains(@class,'chosen-search')]/input")
        search_text_field.send_keys("United King")
        time.sleep(0.5) # let filtering finishing
        # select first selected option
        search_text_field.send_keys(Keys.ENTER)

    def test_chosen_multiple(self):
        # click the box then select one option
        self.driver.find_element_by_xpath("//div[@id='chosen_multiple_chosen']//li[@class='search-field']/input").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='chosen_multiple_chosen']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == "Australia":
                x.click()
                break

        # select another
        self.driver.find_element_by_xpath("//div[@id='chosen_multiple_chosen']//li[@class='search-field']/input").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='chosen_multiple_chosen']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == "United Kingdom":
                x.click()
                break

        # clear all selections
        time.sleep(0.5)
        close_btns = self.driver.find_elements_by_xpath("//div[@id='chosen_multiple_chosen']//ul[@class='chosen-choices']/li[contains(@class,'search-choice')]/a[contains(@class,'search-choice-close')]")
        for cb in close_btns:
            cb.click

        self.driver.find_element_by_xpath("//div[@id='chosen_multiple_chosen']//li[@class='search-field']/input").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='chosen_multiple_chosen']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == "United States":
                x.click()
                break

    def test_clear_chosen(self):
        time.sleep(0.5)
        close_btns = self.driver.find_elements_by_xpath("//div[@id='#{chosen_select_id}']//ul[@class='chosen-choices']/li[contains(@class,'search-choice')]/a[contains(@class,'search-choice-close')]")
        for cb in close_btns:
            cb.click


    def clear_chosen(self, chosen_select_id):
        time.sleep(0.5)
        close_btns = self.driver.find_elements_by_xpath("//div[@id='#{chosen_select_id}']//ul[@class='chosen-choices']/li[contains(@class,'search-choice')]/a[contains(@class,'search-choice-close')]")
        for cb in close_btns:
            cb.click

    def select_chosen_label(self, chosen_select_id, option_label):
        self.driver.find_element_by_xpath("//div[@id='" + chosen_select_id + "']//li[@class='search-field']/input").click()
        available_items = self.driver.find_elements_by_xpath("//div[@id='" + chosen_select_id + "']//div[@class='chosen-drop']//li[contains(@class,'active-result')]")
        for x in available_items:
            if x.text == option_label:
                x.click()
                break

    def test_wrap_chosen_in_reusable_functions(self):
        self.driver.get("file:" + self.site_url() + "/chosen/index.html")
        time.sleep(1)

        self.clear_chosen("chosen_multiple_chosen")
        time.sleep(1)
        self.select_chosen_label("chosen_multiple_chosen", "United States")
        self.select_chosen_label("chosen_multiple_chosen", "Australia")