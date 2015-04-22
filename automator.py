from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

fileToGet = "https://www.youtube.com/watch?v=_FBwVRNOL70"


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('audio/mpeg'))
driver = webdriver.Firefox(firefox_profile=profile)

def youtubeSearcher(song_name, driver):
	driver.get("http://www.youtube.com")
	searchBar = driver.find_element_by_id("masthead-search-term")
	searchBar.send_keys(song_name)
	searchBar.send_keys(Keys.RETURN)
	# try:


	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item-section")))
	
	videoList = driver.find_element_by_css_selector("ol.item-section")
	link = videoList.find_element_by_class_name('yt-lockup-thumbnail')	
	url = link.find_element_by_css_selector('a').get_attribute('href')

	print url
	return url
	# except:
	# 	print "damn"
	# 	return ""

def downloadYoutubeVid(url, driver):
	if (url == ""):
		print 'failed'
		return

	driver.get("http://www.youtube-mp3.org")
	inputArea = driver.find_element_by_id('youtube-url')
	inputArea.clear()
	inputArea.send_keys(url)
	button = driver.find_element_by_id('submit')
	button.click()

	link = driver.find_element_by_id("dl_link")
	element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Download')))
	buttons = link.find_elements_by_tag_name('a')
	print len(buttons)
	for x in buttons:
		if not (x.get_attribute('style')):
			print "success"
			x.click()


downloadYoutubeVid(youtubeSearcher("fashion killa rocky", driver), driver)
# driver.close()
