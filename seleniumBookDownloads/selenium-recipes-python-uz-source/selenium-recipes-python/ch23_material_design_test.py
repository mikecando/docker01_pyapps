import unittest
import time
import random
import os
import os.path
from faker import Faker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MaterialDesignTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.get("https://whenwise.agileway.net")
        
    @classmethod
    def tearDownClass(cls):
        # print("tear down")
        cls.driver.quit()

    def test_materialize_select_list(self):
      elem_id = "businessType"
      option_label = "Physio"
      self.driver.find_element_by_xpath("//select[@id='" + elem_id + "']/..").click()
      time.sleep(0.5)
      self.driver.find_element_by_xpath("//select[@id='" + elem_id + "']/../ul/li/span[text()='" + option_label + "']").click()
      time.sleep(0.5)

    def test_toggle_checkbox(self):
      self.driver.get("https://whenwise.agileway.net/sign-in")
      # the blelow won't work
      # driver.find_element_by_id( "remember_me").click

      # this works
      self.driver.find_element_by_xpath("//input[@id='remember_me']/../span").click()

    def test_check_or_uncheck_checkbox(self):
      self.driver.get("https://whenwise.agileway.net/sign-in")
      # to check
      if not self.driver.find_element_by_id( "remember_me").is_selected():
        self.driver.find_element_by_xpath("//input[@id='remember_me']/../span").click() #

      # uncheck only
      if self.driver.find_element_by_id("remember_me").is_selected():
        self.driver.find_element_by_xpath("//input[@id='remember_me']/../span").click() #

    def test_drag_range_nouislider(self):
      self.driver.get("https://whenwise.agileway.net/biz/superman-driving-school/location/3")
      time.sleep(1)
      self.assertEqual("09:00", self.driver.find_element_by_id("slider-start-time").text)
      minutes = 60 # advance one hour
      step = minutes / 8  # guested number to calcuate steps
      elem = self.driver.find_element_by_class_name("noUi-handle-lower")
      ActionChains(self.driver).drag_and_drop_by_offset(elem, 10 * step, 0).perform()
      time.sleep(0.5)
      self.assertEqual("10:00", self.driver.find_element_by_id("slider-start-time").text)

    def test_verify_toast(self):
      self.driver.get("https://whenwise.agileway.net/sign-up")
      self.driver.find_element_by_id("email").send_keys(Faker().email())
      self.driver.find_element_by_id("password").send_keys("test01")
      self.driver.find_element_by_id("create-account").click()
      # Materialize toast fade in a few seconds
      time.sleep(1)
      toast_text = self.driver.find_element_by_id("toast-container").text
      self.assertIn("Please check your email to activate your account", toast_text)

    def test_verify_modal(self):
      self.driver.get("https://whenwise.agileway.net/biz/4/location/3")
      time.sleep(1)
      self.driver.find_element_by_id("reviews-link").click()
      # wait for modal to show up
      ok_btn_xpath =  "//div[@id='modal-reviews']//a[@id='review-modal-ok']"
      wait = WebDriverWait(self.driver, 4)
      wait.until( EC.visibility_of_element_located( (By.XPATH,ok_btn_xpath) ))

      # verify text
      self.assertIn("It has been a pleasure to", self.driver.find_element_by_id("modal-reviews").text)