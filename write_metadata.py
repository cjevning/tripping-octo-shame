from selenium import webdriver
import eyed3
import sys
import pdb
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3


def write_data(options, song):
	audio = MP3(song, ID3=ID3)

	# add ID3 tag if it doesn't exist
	try:
		audio.delete()
		audio.add_tags()
	except error:
		pass
	audio.tags.add(
	    APIC(
	        encoding=3, # 3 is for utf-8
	        mime='image/jpg', # image/jpeg or image/png
	        type=3, # 3 is for the cover image
	        desc=u'Cover',
	        data=open(options[3]).read()
	    )
	)
	audio.save()
	try:
		meta = EasyID3(song)
	except mutagen.id3.ID3NoHeaderError:
		meta = mutagen.File(filePath, easy=True)
		meta.add_tags()
	meta['title'] = options[0]
	meta['artist'] = options[1]
	if 'soundcloud result' in options[2]:
		meta['album'] = ''	
	else:
		meta['album'] = options[2]

	meta.save()

def collect_options(song_name):
	selected_options = raw_input('choose options: ')
	to_return = []
	option_list = list(selected_options)
	list_len = len(option_list)
	if list_len is 1:
		to_return = option_list
		to_return.extend(option_list)
		to_return.extend(option_list)
	elif list_len > 4:
		for i in range(0, list_len):
			curr_num = option_list[i]
			if curr_num.isdigit(): 
				if i < list_len-2 and not option_list[i+1].isdigit():
					to_return.append(curr_num + 'e')
				else:
					to_return.append(curr_num)
	else:
		to_return = option_list
	print to_return
	return to_return

def edit_prop(thing_to_edit):
	print 'You chose to edit \033[1m' + thing_to_edit + '\033[0m'
	to_return = raw_input('What should it be? ')
	return to_return

def get_data(options, data):
	title = None
	artist = None
	album = None
	art_url = None
	for i in range(0, 4):
		option = options[i]
		edit = False
		if len(option) > 1:
			edit = True
			option = option[0]
		data_to_use = data[int(option)]
		if i is 0:
			title = data_to_use['title']
			if edit:
				title = edit_prop(title)
		elif i is 1:
			artist = data_to_use['artist']
			if edit:
				artist = edit_prop(artist)
		elif i is 2:
			album = data_to_use['album']
			if edit:
				album = edit_prop(album)
		elif i is 3:
			local_art = data_to_use['local_art']
	return [title, artist, album, local_art]







