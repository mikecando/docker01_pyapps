from selenium import webdriver
import time
import os

dir = os.path.dirname(__file__)
edge_path = dir + "\MicrosoftWebDriver.exe"
driver = webdriver.Edge(edge_path)
driver.get("http://sandbox.clinicwise.net")
time.sleep(1)
driver.quit()