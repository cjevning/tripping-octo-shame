import retrieve_metadata as rm
import write_metadata as wm
import song_prepper as sp
import sys
import pdb
from selenium import webdriver

def handle_metadata(name, driver):
	data = rm.get_metadata_for_song(name, driver)
	file_path = './html_pages/' + name + '.html'
	rm.write_html_for_song(file_path, data)
	driver.get('file://' + file_path)
	choices = wm.collect_options(name)
	data_to_use = wm.get_data(choices, data)
	mp3_file = './songs/' + name + '.mp3'
	wm.write_data(data_to_use, mp3_file)

def handle_metadata_multiple(driver):
	songs = sp.parse_file('./downloaded.txt')
	for song in songs:
		handle_metadata(song, driver)

if __name__ == "__main__":
	print 'starting chrome'
	driver = webdriver.Chrome()
	name = '_'.join(sys.argv[1:])
	handle_metadata(driver)
	driver.quit()