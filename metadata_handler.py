import retrieve_metadata as rm
import write_metadata as wm
import song_prepper as sp
import parse_config as pc
import sys
import os
from selenium import webdriver

def handle_metadata(song_path, root, driver):
	splits = song_path.split('/')
	name = splits[len(splits) - 1].rstrip('.mp3')
	data = rm.get_metadata_for_song(song_path, name, driver)
	file_path = root + '/html_pages/' + name + '.html'
	rm.write_html_for_song(file_path, data)
	driver.get('file://' + file_path)
	choices = wm.collect_options(name)
	data_to_use = wm.get_data(choices, data)
	wm.write_data(data_to_use, song_path)

def handle_multiple(dir_path, root_path, driver):
	count = 0
	for root, dirs, files in os.walk(dir_path):
		for file in files:
			if file.endswith(".mp3"):
				file_path = os.path.join(root, file)
				if not rm.already_marked(file_path):
					handle_metadata(file_path, root_path, driver)

if __name__ == "__main__":
	conf = pc.get_config()
	root = conf['root']

	import logger_setup as ls
	logger = ls.get_logger(__name__)

	import clear_folder as cf
	cf.clear(root + '/art_dump')
	cf.clear(root + '/html_pages')
	
	logger.info('starting chrome')
	driver = webdriver.Chrome()
	dir_path = sys.argv[1]
	handle_multiple(driver, dir_path, root)
	driver.quit()

	cf.clear(root + '/art_dump')
	cf.clear(root + '/html_pages')