from selenium import webdriver
import time
import os

if os.name == "nt": 
  driver = webdriver.Ie()
  driver.get("http://testwisely.com/demo")
  time.sleep(1)
  driver.quit()
else:
  print("Non windows platform, skip")
  