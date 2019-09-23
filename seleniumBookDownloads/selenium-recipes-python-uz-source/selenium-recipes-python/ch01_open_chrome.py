from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("http://testwisely.com/demo")
time.sleep(1)
driver.quit()
