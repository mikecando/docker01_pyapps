import unittest
import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AJAXTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get("http://testwisely.com/demo/netbank")

    def tearDown(self):
        self.driver.switch_to.default_content()

    def test_wait_specified_time_for_ajax(self):
        Select(self.driver.find_element_by_name("account")).select_by_visible_text("Cheque")
        self.driver.find_element_by_id("rcptAmount").send_keys("250")
        self.driver.find_element_by_xpath("//input[@value='Transfer']").click()
        time.sleep(10)
        self.assertIn("Receipt No:", self.driver.find_element_by_tag_name("body").text)

    def test_explicit_waits(self):
        Select(self.driver.find_element_by_name("account")).select_by_visible_text("Cheque")
        self.driver.find_element_by_id("rcptAmount").send_keys("250")
        self.driver.find_element_by_xpath("//input[@value='Transfer']").click()
        wait = WebDriverWait(self.driver, 10)
        wait.until( EC.presence_of_element_located((By.ID, "receiptNo")) )
        self.assertTrue(int( self.driver.find_element_by_id("receiptNo").text) > 0)


    def test_implicit_waits(self):
        Select(self.driver.find_element_by_name("account")).select_by_visible_text("Cheque")
        self.driver.find_element_by_id("rcptAmount").send_keys("250")
        self.driver.find_element_by_xpath("//input[@value='Transfer']").click()
        self.driver.implicitly_wait(10) # seconds
        self.assertTrue(int( self.driver.find_element_by_id("receiptNo").text) > 0)
        self.driver.implicitly_wait(0) # reset, don't wait any more

    def test_polling_with_programming(self):
        Select(self.driver.find_element_by_name("account")).select_by_visible_text("Cheque")
        self.driver.find_element_by_id("rcptAmount").send_keys("250")
        self.driver.find_element_by_xpath("//input[@value='Transfer']").click() # AJAX
        timeout = 10  # can change
        start_time = datetime.datetime.now()
        # print( (datetime.datetime.now() - start_time).seconds )
        the_error_occurred = None
        while ( (datetime.datetime.now() - start_time).seconds < timeout ):
            try:
                self.assertTrue( int(self.driver.find_element_by_id("receiptNo").text) > 0 )
                the_error_occurred = None
                break
            except:
                e = sys.exc_info()[0]
                the_error_occurred = e
                time.sleep(1) # polling interval
        if (the_error_occurred):
            self.assertTrue( int(self.driver.find_element_by_id("receiptNo").text) > 0 )

    def wait_for_ajax_complete(self, max_seconds):
        count = 0
        while (count < max_seconds):
            count += 1
            is_ajax_complete = self.driver.execute_script("return window.jQuery != undefined && jQuery.active == 0");
            if is_ajax_complete:
                return
            else:
                time.sleep(1)
        raise Exception("Timed out waiting for AJAX call after %i seconds" % max_seconds)

    def test_wait_ajax_jquery(self):
        self.driver.get("http://travel.agileway.net")
        # ...
        self.driver.find_element_by_id("username").send_keys("agileway")
        self.driver.find_element_by_id("password").send_keys("testwise")
        self.driver.find_element_by_xpath("//input[@value='Sign in']").click()
        self.driver.find_element_by_xpath("//input[@name='tripType' and @value='oneway']").click()
        Select(self.driver.find_element_by_name("fromPort")).select_by_visible_text("New York")
        Select(self.driver.find_element_by_name("toPort")).select_by_visible_text("Sydney")
        Select(self.driver.find_element_by_name("departDay")).select_by_visible_text("04")
        Select(self.driver.find_element_by_name("departMonth")).select_by_visible_text("March 2016")
        self.driver.find_element_by_xpath("//input[@value='Continue']").click()
        time.sleep(1)
        self.driver.find_element_by_name("passengerFirstName").send_keys("Wise")
        self.driver.find_element_by_name("passengerLastName").send_keys("Tester")
        self.driver.find_element_by_xpath("//input[@value='Next']").click()
        self.driver.find_element_by_xpath("//input[@name='card_type' and @value='visa']").click()
        self.driver.find_element_by_name("card_number").send_keys("4000000000000000")
        Select(self.driver.find_element_by_name("expiry_year")).select_by_visible_text("2016")
        self.driver.find_element_by_xpath("//input[@value='Pay now']").click()
        self.wait_for_ajax_complete(10)
        self.assertIn("Booking number", self.driver.page_source)

