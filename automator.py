from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fileToGet = "https://www.youtube.com/watch?v=_FBwVRNOL70"
driver = webdriver.Chrome()

def youtubeSearcher(song_name):
	driver.get("http://www.youtube.com")
	searchBar = driver.find_element_by_id("masthead-search-term")
	searchBar.send_keys(song_name)
	searchBar.send_keys(Keys.RETURN)

	driver.close()
