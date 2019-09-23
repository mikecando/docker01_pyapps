import unittest
import time
import random
import os
import urllib

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class RichTextEditorTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("In tearDown")
        cls.driver.quit()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def test_tinymce(self):
        self.driver.get("file:" + self.site_url() + "/tinymce-4.1.9/tinyice_demo.html")
        self.driver.switch_to.frame("mce_0_ifr")
        editor_body = self.driver.find_element_by_css_selector("body")
        self.driver.execute_script("arguments[0].innerHTML = '<h1>Heading</h1> HTML'", editor_body)
        time.sleep(1)
        editor_body.send_keys("New content")
        time.sleep(1)
        editor_body.clear()

        # setting html content
        self.driver.execute_script("arguments[0].innerHTML = '<p>one</p><p>two</p>'", editor_body)

        # click TinyMCE editor's 'Numbered List' button
        # switch out then can drive controls on the main page
        self.driver.switch_to.default_content()
        tinymce_btn_numbered_list = self.driver.find_element_by_css_selector(".mce-btn[aria-label='Numbered list'] button")
        tinymce_btn_numbered_list.click()

        # Insert
        self.driver.execute_script("tinyMCE.activeEditor.insertContent('<p>Brisbane</p>')")

    def test_code_mirror(self):
        self.driver.get("file:" + self.site_url() + "/codemirror-5.1/demo/xmlcomplete.html")
        elem = self.driver.find_element_by_class_name("CodeMirror-scroll")
        elem.click()
        time.sleep(0.5)
        # elem.send_keys does not work
        ActionChains(self.driver).send_keys("<A>").perform()

    def test_summernote(self):
        self.driver.get("file:" + self.site_url() + "/summernote-0.6.3/demo.html")
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//div[@class='note-editor']/div[@class='note-editable']").send_keys("Text")
        self.driver.find_element_by_xpath("//button[@data-event='insertUnorderedList']").click()
        self.driver.find_element_by_xpath("//button[@data-event='codeview']").click()
        self.driver.find_element_by_xpath("//textarea[@class='note-codable']").send_keys("\n<p>HTML</p>")

    def test_ck_editor(self):
        self.driver.get("file:" + self.site_url() + "/ckeditor-4.4.7/samples/uicolor.html")
        time.sleep(1) # wait JS to load
        ckeditor_frame = self.driver.find_element_by_class_name('cke_wysiwyg_frame')
        self.driver.switch_to.frame(ckeditor_frame)
        editor_body = self.driver.find_element_by_tag_name('body')
        editor_body.send_keys("Selenium Recipes\n by Zhimin Zhan")
        time.sleep(1)

        # Clear content Another Method Using ActionBuilder to clear()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        ActionChains(self.driver).send_keys(Keys.BACK_SPACE).perform()

        self.driver.switch_to.default_content()
        self.driver.find_element_by_class_name("cke_button__numberedlist").click() # numbered list
