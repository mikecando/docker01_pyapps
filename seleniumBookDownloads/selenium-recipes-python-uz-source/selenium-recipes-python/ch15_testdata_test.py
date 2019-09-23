import unittest
import datetime
import random
import os
import urllib
import sqlite3
import string
from selenium import webdriver
from faker import Faker

class TestDataTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("In tearDown")
        cls.driver.quit()

    def setUp(self):
        self.driver.get("file:" + self.site_url() + "/text_field.html")

    # helper function to return local test site url for this book
    def site_url(self):
        site_path = os.path.dirname(os.path.realpath(__file__)) + "/../site"
        return site_path

    def today(self, format = "%Y-%m-%d"):
        return datetime.date.today().strftime(format)

    def yesterday(self, format = "%Y-%m-%d"):
        return (datetime.date.today() - datetime.timedelta(days=1)).strftime(format)

    def tomorrow(self, format = "%Y-%m-%d"):
        return (datetime.date.today() + datetime.timedelta(days=1)).strftime(format)

    def days_from_now(self, days, format = "%Y-%m-%d"):
        return (datetime.date.today() + datetime.timedelta(days=days)).strftime(format)

    def days_before(self, days, format = "%Y-%m-%d"):
        return (datetime.date.today() - datetime.timedelta(days=days)).strftime(format)

    def random_number(self, start_num, end_num):
        return random.randint(start_num, end_num)

    def test_get_date_dynamically(self):
        print(datetime.date.today())  # => 2015-04-14
        print(datetime.datetime.now()) # =>  2015-04-14 18:49:48.154616
        print(self.today())       # 2015-04-14
        print(self.today("%m/%d/%Y"))
        print(self.yesterday())   # 2015-04-13
        print(self.tomorrow())    # 2015-04-15
        print(self.today("%d/%m/%Y")) #=> 14/04/2015
        print(self.days_from_now(3)) # 2015-04-17
        print(self.days_before(3)) # 2015-04-11
        self.driver.find_element_by_id("user").send_keys(self.days_from_now(3))

    def test_random_boolean(self):
        # print(random.choice([True, False]))
        self.driver.get("file:" + self.site_url() + "/radio_button.html")
        random_value = "male" if random.choice([True, False]) else "female"
        elem = self.driver.find_element_by_xpath("//input[@type='radio' and @name='gender' and @value='" + random_value + "']")
        elem.click()

    def test_random_number_in_range(self):
        print(random.randint(10, 99)) # a number between 10 and 99 (inclusive), will be different each run

    def test_random_character(self):
        print(random.choice(string.ascii_letters))   # eg. 't' or 'A'
        print(random.choice(string.ascii_lowercase))
        print(random.choice(string.ascii_uppercase))
        print(chr(random.randint(97, 122))) # lower case, a..z
        print(chr(random.randint(65, 90)))  # upcase, A..Z


    def test_random_string(self):
        # generate 10 characters lower case string
        print(''.join(random.choice(string.ascii_lowercase) for _ in range(10)))

        # generate a password with Mixed case + digits exactly 8 characters
        random.choice(string.ascii_uppercase) + random.choice(string.digits) + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        # 'D1cmuqry'

    def test_random_string_in_collection(self):
        print(random.sample(["Yes", "No", "Maybe"], 1))

    def test_generate_fixed_file_size(self):
        with open( os.path.join( os.path.dirname(os.path.realpath(__file__)), "tmp", "2MB.txt") , 'w') as f:
            f.write(1024 * 1024 * 2 * '0')

    def test_retrieve_from_sqlite3_database(self):
        db = sqlite3.connect( os.path.join( os.path.dirname(os.path.realpath(__file__)), "testdata", "sample.db"))
        # Users table: with login, name, age
        cursor = db.cursor()
        oldest_user_login = None
        cursor.execute( "select * from users order by age desc" )
        first_row = cursor.fetchone()
        # print(first_row)
        oldest_user_login = first_row[0]

        self.assertEqual("mark", oldest_user_login)
        self.driver.get("file:" + self.site_url() + "/text_field.html")
        self.driver.find_element_by_id("user").send_keys(oldest_user_login)

    # faker - https://github.com/joke2k/faker
    def test_faker(self):
        fake = Faker()
        print(fake.address()) # 514 Daugherty Plain, Nikolausburgh, DC 30871
        print(fake.name())    # Devonte Stanton
        print(fake.email())   # tyrek.welch@konopelski.biz

