import os
import eyed3
import re
import pdb
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

amazon_dict = {'space_delim':'+', 'search_url':'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=',
			   'table_class':'mp3Tracks', 'by_method':By.ID, 'no_results_locator':'noResultsTitle', 'result_class':'result',
			   'title_locator': 'title', 'artist_locator': 'mp3tArtist', 'album_locator': 'mp3tAlbum'}
soundcloud_dict = {'space_delim':'%20', 'search_url':'https://soundcloud.com/search?q=', 'table_class':'lazyLoadingList__list', 
				   'by_method':By.CSS_SELECTOR, 'no_results_locator':'.sc-type-h2.sc-text', 'result_class':'searchList__item',
				   'title_locator': 'soundTitle__title', 'artist_locator': 'soundTitle__username'}


def get_metadata_for_song(song_name, driver):
	amazon_song_info = get_song_info(driver, song_name, 'amazon')
	soundcloud_song_info = get_song_info(driver, song_name, 'soundcloud')
	all_song_info = amazon_song_info + soundcloud_song_info
	all_info_w_artwork = get_artwork(driver, all_song_info)
	return all_info_w_artwork


def get_song_info(driver, name, source):
	props = amazon_dict if source is 'amazon' else soundcloud_dict
	query = re.sub('_', props['space_delim'], name)
	url = props['search_url'] + query
	print 'getting url: ' + url
	driver.get(url)
	try:
		print 'looking for search results list...'
		table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, props['table_class'])))
		driver.implicitly_wait(2)
	except TimeoutException:
		print "took too long to find results table, checking for failed search..."
		try:
			no_res = table.findElement(props['by_method'], props['no_results_locator'])
			print "yep, no results"
		except Exception,e: 
			print "strange, couldn`t find failed search page either; slow internet maybe?"
		return []
	print 'results table found!'
	#pdb.set_trace()
	rows = table.find_elements_by_class_name(props['result_class'])
	results = []
	for i in range(0, 4):
		try:
			row = rows[i]
		except:
			if i is 0:
				print 'no ' + source + ' results found for ' + name
			else:
				print source + ' search exhausted after ' + str(i) + ' results'
			break
		try:
			title_elem = row.find_element_by_class_name(props['title_locator'])
			title = str(title_elem.text)
			artist = str(row.find_element_by_class_name(props['artist_locator']).text)
			if source is 'amazon': 
				album = str(row.find_element_by_class_name(props['album_locator']).text)
			else:
				album = 'soundcloud result, album unknown'
			details_url = str(title_elem.get_attribute('href'))
			key_title = re.sub(' ', '_', title)
			file_key = key_title + '_' + source + str(i)
			details_dict = {'title':title, 'artist':artist, 'album':album, 'details':details_url, 'file_key':file_key}
			results.append(details_dict)
		except:
			print 'something went wrong getting details, checking for promoted link or user link...'
			try:
				promoted = row.find_element_by_class_name('promotedBadge')
				print 'yep, promoted link. skipping!'
			except:
				print 'not a promoted link'
				try:
					user = row.find_element_by_class_name('userStats')
					print 'yep, user link. skipping!'
				except:
					print 'not a user link either, not sure what`s wrong'
	return results


def return_amazon_art_url(artwork_cont):
	return artwork_cont.find_element_by_css_selector('img').get_attribute('src')

def return_soundcloud_art_url(artwork_cont):
	style = artwork_cont.get_attribute('style')
	splits = style.split(';')
	back_array = [s for s in splits if 'background-image' in s]
	back = str(back_array[0])
	start = back.index('(') + 1
	end = back.index(')')
	https_url = back[start:end]
	return https_url.replace('https', 'http')


def get_artwork(driver, metadata):
	with_arturls = []
	for song_dict in metadata:
		try:
			details_url = song_dict["details"]
			driver.get(details_url)
			if 'amazon' in details_url:
				by_method = By.ID
				locator = 'coverArt_feature_div'
				url_func = return_amazon_art_url
			else:
				by_method = By.CLASS_NAME
				locator = 'image__full'
				url_func = return_soundcloud_art_url
			try:
				artwork_cont = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_method, locator)))
				art_url = url_func(artwork_cont)
				ext = art_url[-3:]
				file_key = song_dict["file_key"]
				file_path = d.root_directory + 'songs/art_dump/' + file_key + '.' + ext
				urllib.urlretrieve(art_url, file_path)
				song_dict['art_url'] = str(art_url)
				song_dict['local_art'] = str(file_path)
				with_arturls.append(song_dict)
			except Exception,e: 
				print 'failed to save artwork for some reason:'
				print e
		except Exception,e: 
			print 'an unexpected error happened somewhere:'
			print e
	return with_arturls



def write_html_for_song(file_path, data):
    with open(file_path, 'w') as myFile:
    	myFile.write('<html><body><table style="text-align:center;"><tr><td><h1>Option</h1></td><td><h1>Title</h1></td><td><h1>Artist</h1></td>')
    	myFile.write('<td><h1>Album</h1></td><td><h1>Artwork</h1></td></tr>')
        for i in range(0, len(data)):
        	myFile.write('<tr><td><h1>')
        	myFile.write(str(i))
        	myFile.write('</h1></td><td><p>')
        	myFile.write(data[i]['title'])
        	myFile.write('</p></td><td><p>')
        	myFile.write(data[i]['artist'])
        	myFile.write('</p></td><td><p>')
        	myFile.write(data[i]['album'])
        	myFile.write('</p></td><td><img src="')
        	myFile.write(data[i]['art_url'])
        	myFile.write('"></td></tr>')
        myFile.write('</table>')
        myFile.write('</body>')
        myFile.write('</html>')






