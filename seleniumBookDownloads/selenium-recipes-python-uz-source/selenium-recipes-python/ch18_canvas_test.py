import unittest
import time
import base64
import random
import os
import urllib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver

class CanvasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path
        
    def test_save_canvas_to_image(self):
        self.driver.get("http://www.chartjs.org/samples/latest/charts/bar/vertical.html")
        time.sleep(1)  # wait canvas is loaded
        canvas_elem = self.driver.find_element_by_xpath("//canvas[@id='canvas']")
        js_extract_canvas = "return arguments[0].toDataURL('image/png').substring(21);"
        canvas_base64 = self.driver.execute_script(js_extract_canvas, canvas_elem)
        canvas_png = base64.b64decode(canvas_base64)
        file_path = "c:\\temp\\saved_canvas.png" if os.name == "nt" else "/Users/zhimin/tmp/saved_canvas.png"
        f = open(file_path, "wb")
        f.write(canvas_png)
        f.close()
        self.assertTrue(os.path.isfile(file_path))


    def test_verify_dynamic_charts(self):
        self.driver.get("file://" + self.site_url() + "/canvas.html")
        canvas_elem = self.driver.find_element_by_id("myChart")
        time.sleep(1) # wait JS to load into Canvas
        self.assertTrue(canvas_elem.is_displayed())

        js_extract_canvas = "return arguments[0].toDataURL('image/png').substring(21);"
        canvas_base64 = self.driver.execute_script(js_extract_canvas, canvas_elem)
        canvas_image_size_1 = len(canvas_base64)

        time.sleep(2)
        canvas_base64 = self.driver.execute_script(js_extract_canvas, canvas_elem)
        canvas_image_size_2 = len(canvas_base64)

        time.sleep(2)
        canvas_base64 = self.driver.execute_script(js_extract_canvas, canvas_elem)
        canvas_image_size_3 = len(canvas_base64)
        
        # verify the images of canvas all different (in size)
        uniq_image_size_list = set([canvas_image_size_1, canvas_image_size_2, canvas_image_size_3])
        self.assertEqual(3, len(uniq_image_size_list))