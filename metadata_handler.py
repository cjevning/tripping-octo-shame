import retrieve_metadata as rm
import write_metadata as wm
import song_prepper as sp
import sys
import pdb
import os
from selenium import webdriver

def handle_metadata(song_path, driver):
	splits = song_path.split('/')
	name = splits[len(splits) - 1].rstrip('.mp3')
	data = rm.get_metadata_for_song(song_path, name, driver)
	file_path = './html_pages/' + name + '.html'
	rm.write_html_for_song(file_path, data)
	driver.get('file://' + file_path)
	choices = wm.collect_options(name)
	data_to_use = wm.get_data(choices, data)
	mp3_file = './songs/' + name + '.mp3'
	wm.write_data(data_to_use, mp3_file)

def handle_multiple(driver, dir_path):
	for root, dirs, files in os.walk(dir_path):
		for file in files:
			if file.endswith(".mp3"):
				handle_metadata(os.path.join(root, file), driver)

if __name__ == "__main__":
	print 'starting chrome'
	driver = webdriver.Chrome()
	dir_path = sys.argv[1]
	handle_metadata(driver, dir_path)
	driver.quit()