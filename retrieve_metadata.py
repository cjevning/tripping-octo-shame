import os
import eyed3
import re
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3
from mutagen import File
import logger_setup as ls
logger = ls.get_logger(__name__)

amazon_dict = {'space_delim':'+', 'search_url':'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=',
			   'table_class':'mp3Tracks', 'by_method':By.ID, 'no_results_locator':'noResultsTitle', 'result_class':'result',
			   'title_locator': 'title', 'artist_locator': 'mp3tArtist', 'album_locator': 'mp3tAlbum'}
soundcloud_dict = {'space_delim':'%20', 'search_url':'https://soundcloud.com/search?q=', 'table_class':'lazyLoadingList__list', 
				   'by_method':By.CSS_SELECTOR, 'no_results_locator':'.sc-type-h2.sc-text', 'result_class':'searchList__item',
				   'title_locator': 'soundTitle__title', 'artist_locator': 'soundTitle__username'}


def get_metadata_for_song(song_path, song_name, driver):
	amazon_song_info = get_song_info(driver, song_name, 'amazon')
	soundcloud_song_info = get_song_info(driver, song_name, 'soundcloud')
	all_song_info = amazon_song_info + soundcloud_song_info
	all_info_w_artwork = get_artwork(driver, all_song_info)
	current_song_info = get_current_metadata(song_path, song_name)
	return current_song_info + all_info_w_artwork

def get_current_metadata(song_path, song_name):
	try:
		tags = ID3(song_path)
	except Exception,e:
		logger.error('couldn`t get tags on the song for this reason:')
		logger.error(e)
		logger.info('skipping')
		return []
	try:
		title = tags["TIT2"].text[0]
	except:
		title = ''
	try:
		artist = tags["TPE1"].text[0]
	except:
		artist = ''
	try:
		album = tags["TALB"].text[0]
	except:
		album = ''
	mfile = File(song_path)
	file_key = song_name + '_default'
	file_path = '-'
	file_url = ''
	try:
		apic = mfile.tags['APIC:']
		mime_sp = apic.mime.split('/')
		ext = mime_sp[len(mime_sp) - 1]

		artwork = apic.data # access APIC frame and grab the image
		
		cwd = os.getcwd()
		file_path = cwd + '/art_dump/' + file_key + '.' + ext

		file_url = 'file://' + file_path

		
		with open(file_path, 'wb') as img:
			img.write(artwork)
	except Exception,e:
		logger.warn('failed to get artwork attached to mp3, probably doesn`t have any. here`s the exception:')
		logger.warn(e)


	song_dict = {'title':title, 'artist':artist, 'album':album, 'local_art':file_path, 'art_url':file_url, 'file_key':file_key}
	return [song_dict]


def get_song_info(driver, name, source):
	props = amazon_dict if source is 'amazon' else soundcloud_dict
	query = re.sub('_', props['space_delim'], name)
	url = props['search_url'] + query
	logger.info('getting url: ' + url)
	driver.get(url)
	try:
		logger.info('looking for search results list...')
		table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, props['table_class'])))
		driver.implicitly_wait(2)
	except TimeoutException:
		logger.error("took too long to find results table, checking for failed search...")
		try:
			thing = driver if source is 'amazon' else table
			no_res = thing.findElement(props['by_method'], props['no_results_locator'])
			logger.info("yep, no results")
		except Exception,e: 
			logger.info("strange, couldn`t find failed search page either; slow internet maybe?")
		return []
	logger.info('results table found!')
	rows = table.find_elements_by_class_name(props['result_class'])
	results = []
	for i in range(0, 4):
		try:
			row = rows[i]
		except:
			if i is 0:
				logger.error('no ' + source + ' results found for ' + name)
			else:
				logger.warn(source + ' search exhausted after ' + str(i) + ' results')
			break
		try:
			title_elem = row.find_element_by_class_name(props['title_locator'])
			title = title_elem.text.encode('utf8') #str(title_elem.text)
			title = re.sub('/', '', title)
			artist = row.find_element_by_class_name(props['artist_locator']).text.encode('utf8') #str(row.find_element_by_class_name(props['artist_locator']).text)
			if source is 'amazon': 
				album = row.find_element_by_class_name(props['album_locator']).text.encode('utf8') #str(row.find_element_by_class_name(props['album_locator']).text)
			else:
				album = 'soundcloud result, album unknown'
			details_url = str(title_elem.get_attribute('href'))
			key_title = re.sub(' ', '_', title)
			file_key = key_title + '_' + source + str(i)
			details_dict = {'title':title, 'artist':artist, 'album':album, 'details':details_url, 'file_key':file_key}
			results.append(details_dict)
		except:
			logger.error('something went wrong getting details, checking for promoted link or user link...')
			try:
				promoted = row.find_element_by_class_name('promotedBadge')
				logger.info('yep, promoted link. skipping!')
			except:
				try:
					user = row.find_element_by_class_name('userStats')
					logger.info('yep, user link. skipping!')
				except:
					logger.info('doesn`t seem to be promoted or user link, not sure what`s wrong')
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
				file_key = song_dict["file_key"].decode('utf8')
				file_path = os.getcwd() + '\\art_dump\\' + file_key + '.' + ext
				urllib.urlretrieve(art_url, file_path)
				song_dict['art_url'] = str(art_url)
				song_dict['local_art'] = file_path.encode('utf8')
				with_arturls.append(song_dict)
			except Exception,e: 
				logger.error('failed to save artwork for some reason:')
				logger.error(e)
		except Exception,e: 
			logger.error('an unexpected error happened somewhere:')
			logger.error(e)
	return with_arturls

def already_marked(file_path):
	try:
		tags = EasyID3(file_path)
	except Exception,e:
		logger.info('no tags on the song, proceed')
		return False
	try:
		marked = tags['website'][0]
		if marked == 'connerjevning.com':
			logger.info('already marked! skipping')
			return True
		else:
			return False
	except:
		logger.info('doesn`t appear to be marked, proceed')
		return False

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





