from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import sys

songs = []
song = raw_input("Enter song name and artist. Press Enter with empty string to run: ")

while (len(song) < 1):
	song = raw_input("Enter at least 1 song name and artist. Press Enter with empty string to run: ")

while (len(song) > 0):
	songs.append(song)
	song = raw_input("Enter song name and artist. Press Enter with empty string to run: ")
	

profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.dir', '~/Music/recentDownloads')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('audio/mpeg'))


print "Starting up Firefox. Please wait"
driver = webdriver.Firefox(firefox_profile=profile)

def youtubeSearcher(songs, driver):
	driver.get("http://www.youtube.com")

	print "Beginning your search"
	urls = []

	for song_name in songs:
		searchBar = driver.find_element_by_id("masthead-search-term")
		searchBar.clear()
		searchBar.send_keys(song_name)
		searchBar.send_keys(Keys.RETURN)
		try:
			element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item-section")))
	
			videoList = driver.find_element_by_css_selector("ol.item-section")
			link = videoList.find_element_by_class_name('yt-lockup-thumbnail')	
			urls.append(link.find_element_by_css_selector('a').get_attribute('href'))
		except:
			print "there was an error finding " + song_name
	return urls

def downloadYoutubeVid(url, driver):
	if (url == ""):
		print 'failed'
		return

	inputArea = driver.find_element_by_id('youtube-url')
	inputArea.clear()
	inputArea.send_keys(url)
	button = driver.find_element_by_id('submit')
	button.click()

	link = driver.find_element_by_id("dl_link")
	element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Download')))
	buttons = link.find_elements_by_tag_name('a')
	for x in buttons:
		if not (x.get_attribute('style')):
			x.click()
			return

allURLs = youtubeSearcher(songs, driver)
driver.get("http://www.youtube-mp3.org")
for url in allURLs:
	downloadYoutubeVid(url, driver)

time.sleep(10*(1 + len(allURLs) / 3))
driver.close()
