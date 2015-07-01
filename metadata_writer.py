from selenium import webdriver
import eyed3
import sys
from itertools import groupby

def write_data(options):
	audiofile = eyed3.load("song.mp3")
	audiofile.tag.artist = u"Nobunny"
	audiofile.tag.album = u"Love Visions"
	audiofile.tag.album_artist = u"Various Artists"
	audiofile.tag.title = u"I Am a Girlfriend"
	audiofile.tag.track_num = 4

	audiofile.tag.save()

def collect_options(song_name):
	selected_options = raw_input('choose options: ')
	option_list = [''.join(g) for k, g in groupby(selected_options, key=str.isdigit)]
	print option_list
	return options

if __name__ == "__main__":
	print 'starting chrome'
	driver = webdriver.Chrome()
	driver.maximize_window()
	name = '_'.join(sys.argv[1:])
	file_path = 'file:///Users/cjevning/Desktop/songs/html_pages/' + name + '.html'
	driver.get(file_path)
	collect_options(name)
	driver.quit()
