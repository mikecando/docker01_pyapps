import unittest
import time
import os
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class SelectListRecipeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/select_list.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_select_option_by_label(self):
        Select(self.driver.find_element_by_name("car_make")).select_by_visible_text("Volvo (Sweden)")

    def test_select_option_by_value(self):
        Select(self.driver.find_element_by_name("car_make")).select_by_value("audi")

    def test_select_by_text_via_iterating_options(self):
        my_select = self.driver.find_element_by_id("car_make_select")
        for option in my_select.find_elements_by_tag_name("option"):
            if option.text == "Volvo (Sweden)":
                option.click()
                break

    def test_assert_option_in_select_list(self):
        my_select = self.driver.find_element_by_id("car_make_select")
        select_texts = [ option.text for option  in my_select.find_elements_by_tag_name("option") ]
        self.assertIn("Honda (Japan)", select_texts)

        select_values = [ option.get_attribute("value") for option  in my_select.find_elements_by_tag_name("option") ]
        print(select_values)
        self.assertIn("audi", select_values)

    def test_assert_value_of_select_list(self):
        the_select = Select(self.driver.find_element_by_name("car_make"))
        the_select.select_by_visible_text("Volvo (Sweden)")
        self.assertEqual(the_select.first_selected_option.get_attribute("value"), "volvo")

    def test_assert_selected_option_of_select_list(self):
        the_select = Select(self.driver.find_element_by_id("car_make_select"))
        the_select.select_by_value("audi")
        self.assertEqual(the_select.first_selected_option.text, "Audi (Germany)")

    def test_select_multiple(self):
        Select(self.driver.find_element_by_name("test_framework")).select_by_visible_text("Selenium")
        Select(self.driver.find_element_by_name("test_framework")).select_by_visible_text("RWebSpec")

    def test_deselect_option_multiple(self):
        select_box = Select(self.driver.find_element_by_name("test_framework"))
        select_box.select_by_visible_text("Selenium")
        select_box.select_by_value("rwebspec")
        select_box.deselect_by_visible_text("RWebSpec") # by label
        select_box.deselect_by_index(3) # :index

    def test_clear_multiple_selects(self):
        select_box = Select(self.driver.find_element_by_name("test_framework"))
        select_box.select_by_visible_text("Selenium")
        select_box.select_by_visible_text("RWebSpec")
        select_box.deselect_all()

    def test_assert_multiple_selected_options(self):
        select_box = Select(self.driver.find_element_by_name("test_framework"))
        select_box.select_by_visible_text("Selenium")
        select_box.select_by_visible_text("RWebSpec")

        selected = select_box.all_selected_options
        self.assertEqual(2, len(selected))
        self.assertEqual("RWebSpec", selected[0].text) # based on displaying order
        self.assertEqual("Selenium", selected[1].text)

