import unittest
import time
import os
import urllib
from selenium import webdriver

class LinkRecipeTestCase(unittest.TestCase):
    
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

    def setUp(self):
        url = "file:" + self.site_url() + "/../site/link.html"
        self.driver.get(url)

    def test_click_link_by_text(self):
        self.driver.find_element_by_link_text("Recommend Selenium").click()

    def test_click_link_by_id(self):
        self.driver.find_element_by_id("recommend_selenium_link").click()

    def test_click_link_by_partial_text(self):
        self.driver.find_element_by_partial_link_text("Recommend Selenium").click()

    def test_click_link_by_xpath(self):        
        self.driver.find_element_by_xpath("//p/a[text()='Recommend Selenium']").click()
        self.driver.get("file:" + self.site_url() + "/link.html")

    def test_click_link_by_xpath_using_function(self):
        # Click the link (two on the same page), click the second one by narrowing down with parent div
        # using XPath contains() functions
        self.driver.find_element_by_xpath('//div[contains(text(), "Second")]/a[text()="Click here"]').click()

    def test_click_second_link_with_exact_text_using_array_index(self):
        print(self.driver.find_elements_by_link_text("Same link").__class__)
        self.assertEqual( len(self.driver.find_elements_by_link_text("Same link")), 2)
        self.driver.find_elements_by_link_text("Same link")[1].click() # second link
        self.assertIn("second link page", self.driver.page_source)

    def test_click_second_link_with_exact_text_using_css_locator(self):
        self.driver.find_element_by_css_selector("p  > a:nth-child(3)").click()
        self.assertIn("second link page", self.driver.page_source)

    def test_links_opening_another_window_or_tab(self):
        current_url = self.driver.current_url
        # Ruby using ["href"]
        new_window_url = self.driver.find_element_by_link_text("Open new window").get_attribute("href")
        self.driver.get(new_window_url)
        # ... testing on new site
        self.driver.find_element_by_name("name").send_keys("sometext")
        self.driver.get(current_url) # back
  

    # Retrieve link other attributes
    #
    def test_retrieve_common_link_details(self):
        self.assertIn("/site/index.html", self.driver.find_element_by_link_text("Recommend Selenium").get_attribute("href"))
        self.assertEqual(self.driver.find_element_by_link_text("Recommend Selenium").get_attribute("id"), "recommend_selenium_link")
        self.assertEqual(self.driver.find_element_by_id("recommend_selenium_link").text, "Recommend Selenium")
        self.assertEqual(self.driver.find_element_by_id("recommend_selenium_link").tag_name, "a")

    def test_retrieve_advanced_link_attributes(self):
        self.assertEqual(self.driver.find_element_by_id("recommend_selenium_link").get_attribute("style"), "font-size: 14px;")
        # Please note using attribute_value("style") won't work
        self.assertEqual(self.driver.find_element_by_id("recommend_selenium_link").get_attribute("data-id"), "123")
  
    # Verify links
    #
    def test_verify_link_present(self):
        self.assertTrue(self.driver.find_element_by_link_text("Recommend Selenium").is_displayed())
        self.assertTrue(self.driver.find_element_by_id("recommend_selenium_link").is_displayed())
  
    def test_verify_link_displayed_or_hidden(self):
        self.assertTrue(self.driver.find_element_by_link_text("Recommend Selenium").is_displayed())
        self.assertTrue(self.driver.find_element_by_id("recommend_selenium_link").is_displayed())

        self.driver.find_element_by_link_text("Hide").click()
        time.sleep(1)
        try:
          # different from Watir, selenium returns element not found
          self.assertFalse(self.driver.find_element_by_link_text("Recommend Selenium").is_displayed())
        except:
          print("[Selenium] The hidden link cannot be found")

        self.driver.find_element_by_link_text("Show").click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element_by_link_text("Recommend Selenium").is_displayed())
