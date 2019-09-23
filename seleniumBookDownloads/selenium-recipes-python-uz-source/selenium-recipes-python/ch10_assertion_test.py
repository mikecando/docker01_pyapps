import unittest
import time
import os
import urllib
from selenium import webdriver

class AssertionRecipeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/assert.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_assert_title(self):
        self.assertEqual("Assertion Test Page", self.driver.title)

    def test_assert_page_text(self):
        matching_str = "Text assertion with a  (tab before), and \n(new line before)!"
        self.assertIn(matching_str, self.driver.find_element_by_tag_name("body").text)

    def test_assert_page_source(self):
        self.assertIn("Text assertion with a  (<b>tab</b> before), and \n(new line before)!", self.driver.page_source)

    def test_assert_label_text(self):
        self.assertEqual("First Label", self.driver.find_element_by_id("label_1").text)

    def test_assert_span_text(self):
        self.assertEqual("Second Span", self.driver.find_element_by_id("span_2").text)

    def test_assert_text_in_div(self):
        self.assertEqual("TestWise", self.driver.find_element_by_id("div_child_1").text)
        self.assertEqual("Wise Products\nTestWise\nBuildWise", self.driver.find_element_by_id("div_parent").text)

    def test_assert_div_html(self):
        the_element = self.driver.find_element_by_id("div_parent")
        the_element_html = self.driver.execute_script("return arguments[0].outerHTML;", the_element)
        print(the_element_html)
        self.assertEqual(the_element_html, '<div id="div_parent">\n	   Wise Products\n	   <div id="div_child_1">\n	   	 TestWise\n	   </div>\n	   <div id="div_child_2">\n	   	 BuildWise\n	   </div>\n	 </div>')

    def test_assert_text_in_table(self):
        the_element = self.driver.find_element_by_id("alpha_table")
        self.assertEqual(the_element.text, "A B\na b")    # watir => "AB\r\nab"
        the_element_html = self.driver.execute_script("return arguments[0].outerHTML;", the_element)
        self.assertIn("<td id=\"cell_1_1\">A</td>", the_element_html)

    def test_assert_text_in_table_cell_by_id(self):
        self.assertEqual("A", self.driver.find_element_by_id("cell_1_1").text)

    # NOTE: the tbody is not in page source, the index starting from 1
    def test_assert_text_in_table_cell_with_coords(self):
        self.assertEqual(self.driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]").text, "b")

    def test_assert_text_in_table_row(self):
        # Watir IE => "AB"
        self.assertEqual(self.driver.find_element_by_id("row_1").text, "A B")

    def test_assert_image_presents(self):
        self.assertTrue(self.driver.find_element_by_id("next_go").is_displayed())

    def test_assert_element_location_and_width(self):
        image_elem = self.driver.find_element_by_id("next_go")
        self.assertEqual(46, image_elem.size["width"])
        self.assertTrue(image_elem.location["x"] > 100)

    def test_assert_element_css_style(self):
        elem = self.driver.find_element_by_id("highlighted")
        self.assertEqual("15px", elem.value_of_css_property("font-size"))
        self.assertEqual("rgba(206, 218, 227, 1)", elem.value_of_css_property("background-color"))

    def test_assert_javascript_errors(self):
        # a page with JavaScript errors
        self.driver.get("http://testwisely.com/demo/customer-interview")
        log_entries = self.driver.get_log("browser")
        self.assertEqual(1, len(log_entries))
        self.assertIn("net::ERR_CONNECTION_REFUSED", str(log_entries[0]))

        # a page without errors
        self.driver.get("http://testwisely.com/demo")
        log_entries = self.driver.get_log("browser")
        self.assertEqual(0, len(log_entries))
