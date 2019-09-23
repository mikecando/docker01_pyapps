import unittest
import time
import os

from selenium import webdriver

class BrowserProxyTestCase(unittest.TestCase):

    def test_change_firefox_profile(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference('network.proxy.type',  1)
        # http://kb.mozillazine.org/Network.proxy.type
        fp.set_preference('network.proxy.http', "myproxy.com")
        fp.set_preference('network.proxy.http_port',  3128)
        driver = webdriver.Firefox(firefox_profile=fp)
        driver.get("http://testwisely.com/demo")
        driver.quit()

 