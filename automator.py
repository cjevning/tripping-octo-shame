from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fileToGet = "https://www.youtube.com/watch?v=_FBwVRNOL70"
driver = webdriver.Chrome()
driver.get("www.youtube.com")