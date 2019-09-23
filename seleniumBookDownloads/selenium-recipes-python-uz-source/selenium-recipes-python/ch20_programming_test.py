import unittest
import time
import random
import os
import os.path
import urllib
import csv
import xlrd  # pip install xlrd, a library for extract data from Excel
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

class ProgrammingTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        # print("tear down")
        cls.driver.quit()

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path


    # Using following syntax for in complete test, let it fail

    #    def test_incomplete_test(self):
    #        raise Exception("To be done")

    def test_catch_exception(self):
        try:     # try block
           new_driver = webdriver.Firefox()
           new_driver.get("http://sandbox.clinicwise.net")
           new_driver.find_element_by_id("not_exists").click();
        except:  # optionally: `except Exception as ex:`
           print("caught, this time I ignore")
        finally: # always get executed
           new_driver.quit()  # close the browser regardless pass or fail


    def test_read_external_file_absolute_path(self):
        input_file = "c:\\temp\\in.xml" if os.name == "nt" else "/Users/zhimin/tmp/in.xml" #bad
        file_content = open(input_file).read()
        print(file_content)

    def test_read_external_file_relative_path(self):
        input_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), "testdata",  'in.xml')
        self.assertTrue(os.path.isfile(input_file))

    def test_setting_vs_typing_text_in_text_field(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")
        # no typing, direct set
        self.driver.execute_script("$('#user').val('TestWise')")
        # vs
        time.sleep(2)
        elem = self.driver.find_element_by_id("user")
        elem.clear()
        elem.send_keys("Test")
        time.sleep(1)
        elem.send_keys("Wise")

    # more detail: http://watirwebdriver.com/sending-special-keys/
    def test_send_enter_or_special_characters_to_text_field(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")
        elem = self.driver.find_element_by_id("user")
        elem.clear()
        elem.send_keys("agileway")
        time.sleep(1) # sleep for seeing the effect

        # select all (Ctrl+A) then press backspace
        elem.send_keys([Keys.CONTROL, 'a'], Keys.BACK_SPACE)
        time.sleep(1)
        elem.send_keys("testwisely")
        time.sleep(1)
        elem.send_keys(Keys.ENTER) # submit the form

    def test_enter_and_check_unicode(self):
        self.driver.get("file:" + self.site_url() + "/assert.html")
        self.assertEqual(self.driver.find_element_by_id("unicode_test").text, "空気")
        self.driver.get("file:" + self.site_url() + "/text_field.html")
        self.driver.find_element_by_id("user").send_keys("проворный")

    def test_dynamically_generated_prefix_in_element_name(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")
        self.driver.find_element_by_name("ctl00$m$g_dcb0d043_e7f0_4128_99c6_71c113f45dd8$ctl00$tAppName").send_keys("full name")
        self.driver.find_element_by_name("ctl00$m$g_dcb0d043_e7f0_4128_99c6_71c113f45dd8$ctl00$tAppName").clear()
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[contains(@name, 'AppName')]").send_keys("I still can")

    def test_copied_text_not_exact_match(self):
        self.driver.get("http://testwisely.com/demo/assertion")
        # tags in source not in text
        self.assertIn("BOLD Italic", self.driver.find_element_by_tag_name("body").text)
        self.assertIn("<b>BOLD</b>  <i>Italic</i>",self.driver.page_source)

        # HTML entities in source but shown as space in text
        self.assertIn("assertion  \n(new line before)", self.driver.find_element_by_tag_name("body").text)

        # note the second character after assertion is non-breaable space (&nbsp;)
        if self.driver.capabilities["browserName"] == "firefox":
            # different behaviour on Firefox (v25)
            self.assertIn("assertion &nbsp;\n(new line before)", self.driver.page_source)
        else:
            self.assertIn("assertion  \n(new line before)", self.driver.page_source)


    def test_data_driven_test_csv(self):
        csv_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), "testdata",  'users.csv')
        f = open(csv_file, 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                # print(row)
                login, password, expected_text = row[1], row[2], row[3]
                if login == "LOGIN":
                    continue    # ignore first head row
                self.driver.get("http://travel.agileway.net")
                self.driver.find_element_by_name("username").send_keys(login)
                self.driver.find_element_by_name("password").send_keys(password)
                self.driver.find_element_by_name("username").submit()
                self.assertIn(expected_text, self.driver.find_element_by_tag_name("body").text)
                try:
                    self.driver.find_element_by_link_text("Sign off").click()
                except:
                    # ignore
                    print("Ignore if unable to sign off")
        finally:
            f.close

    def test_data_driven_test_excel(self):
        csv_file = os.path.join( os.path.dirname(os.path.realpath(__file__)), "testdata",  'users.xls')
        workbook = xlrd.open_workbook(csv_file)
        worksheet = workbook.sheet_by_name('users') # workbook.sheet_by_index(0)
        num_rows = worksheet.nrows - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            # print(row)
            login, password, expected_text = row[1].value, row[2].value, row[3].value
            if login == "LOGIN":
                continue    # ignore first head row
            self.driver.get("http://travel.agileway.net")
            self.driver.find_element_by_name("username").send_keys(login)
            self.driver.find_element_by_name("password").send_keys(password)
            self.driver.find_element_by_name("username").submit()
            self.assertIn(expected_text, self.driver.find_element_by_tag_name("body").text)
            try:
                self.driver.find_element_by_link_text("Sign off").click()
            except:
                # ignore
                print("Ignore if unable to sign off")

    def test_scroll_to_the_bottom_of_page(self):
        self.driver.get("https://clinicwise.net/pricing")
        # JavaScript API
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Send keyboard command
        self.driver.find_element_by_tag_name("body").send_keys([Keys.CONTROL, Keys.END])
        # Or
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.END).key_up(Keys.CONTROL).perform()

    def test_verify_search_results_order(self):
        self.driver.get("file:" + self.site_url() + "/data_grid.html")
        time.sleep(1)
        self.driver.find_element_by_id("heading_product").click()  # first asc
        first_cells = self.driver.find_elements_by_xpath("//tbody/tr/td[1]")
        product_names = [v.text for v in first_cells]
        # print(product_names);
        self.assertEqual(product_names, sorted(product_names))

        self.driver.find_element_by_id("heading_product").click()  # change sorting
        time.sleep(1)
        first_cells = self.driver.find_elements_by_xpath("//tbody/tr/td[1]")
        product_names = [v.text for v in first_cells]
        self.assertEqual(product_names, sorted(product_names, reverse=True))

    def test_verify_uniqueness_of_a_set_of_data(self):
        self.driver.get("file:" + self.site_url() + "/data_grid.html")
        second_cells = self.driver.find_elements_by_xpath("//tbody/tr/td[2]")
        years_released =  [v.text for v in second_cells]
        # len(set(one_list)) removes duplicates
        self.assertEqual(len(years_released), len(list(set(years_released))))

    def test_table_with_hidden_rows(self):
        self.driver.get("file:" + self.site_url() + "/data_grid.html")
        rows = self.driver.find_elements_by_xpath("//table[@id='grid']/tbody/tr")
        self.assertEqual(4, len(rows))
        first_product_name = self.driver.find_element_by_xpath("//table[@id='grid']//tbody/tr[1]/td[1]").text
        self.assertEqual("ClinicWise", first_product_name)
        self.driver.find_element_by_xpath("//table[@id='grid']//tbody/tr[1]/td/button").click()

        self.driver.find_element_by_id("test_products_only_flag").click() # Filter results
        time.sleep(0.2)
        # Error: Element is not currently visible
        # driver.find_element_by_xpath("//table[@id='grid']//tbody/tr[1]/td/button").click()

        displayed_rows = self.driver.find_elements_by_xpath("//table[@id='grid']//tbody/tr[not(contains(@style,'display: none'))]")
        self.assertEqual(2, len(displayed_rows))
        first_row_elem = displayed_rows[0]
        new_first_product_name = first_row_elem.find_element_by_xpath("td[1]").text
        self.assertEqual("BuildWise", new_first_product_name)
        first_row_elem.find_element_by_xpath("td/button").click()

    def test_extract_dynamic_pattern_text_with_regex(self):
        self.driver.get("file:" + self.site_url() + "/coupon.html")
        self.driver.find_element_by_id("get_coupon_btn").click()
        coupon_text = self.driver.find_element_by_id("details").text
        # Your coupon code: <b>H8ZVTA</b> used by <b>2015-11-9</b>
        import re
        searchObj = re.search( r'coupon code:\s+(\w+) used by\s([\d|-]+)', coupon_text, re.M|re.I)
        if searchObj:
          coupon_code = searchObj.group(1)
          expiry_date = searchObj.group(2)
          print(coupon_code)
          print(expiry_date)
          self.driver.find_element_by_name( "coupon").send_keys(coupon_code)
        else:
          raise Exception("Error: no valid coupon returned")

    def test_extract_text_with_regex(self):
        self.driver.get("file:" + self.site_url() + "/index.html")
        import re
        ver = re.findall(r'<!-- Version: (.*?) -->', self.driver.page_source)
        print(ver)  # ['2.19.1.9798']
        self.assertEqual(4, len(ver[0].split('.')))
        self.assertEqual("2", ver[0].split(".")[0])  # major version
        self.assertEqual("19", ver[0].split(".")[1]) # minor version

        app_vers = re.findall(r'<!-- (\w+) Version: (.*?) -->', self.driver.page_source)
        print(app_vers) # [('TestWise', '4.7.1'), ('ClinicWise', '3.0.6')]
        self.assertEqual("ClinicWise", app_vers[1][0])
