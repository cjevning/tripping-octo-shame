from selenium import webdriver
import eyed3
import sys
#from mutagen import Picture
from mutagen.mp3 import MP3
from mutagen import File
from mutagen.id3 import ID3, APIC, error, ID3NoHeaderError
from mutagen.flac import FLAC, Picture
from mutagen.easyid3 import EasyID3
import mutagen


def write_data(options, song):
	audio = MP3(song, ID3=ID3)

	# add ID3 tag if it doesn't exist
	try:
		audio.delete()
		audio.add_tags()
	except error:
		pass
	audio.save()

	try:
		meta = EasyID3(song)
	except ID3NoHeaderError:
		meta = mutagen.File(song, easy=True)
		meta.add_tags()
	if options[0] is not None:
		meta['title'] = options[0].decode('utf8')
	if options[1] is not None:
		meta['artist'] = options[1].decode('utf8')
	if options[2] is not None:
		if 'soundcloud result' in options[2] or options[2] is '-':
			meta['album'] = 'Promo Singles'	
		else:
			meta['album'] = options[2].decode('utf8')
	ws = 'connerjevning.com'
	if len(options) is 5:
		ws += '/'
	meta['website'] = ws
	meta.save()


	
	if options[3] is not '-':
		# audio = File(song)
		# image = Picture()
		# image.type = 3
		# if options[3].endswith('png'):
		# 	mime = 'image/png'
		# else:
		# 	mime = 'image/jpeg'
		# image.desc = 'front cover'
		# with open(options[3], 'rb') as f: # better than open(albumart, 'rb').read() ?
		# 	image.data = f.read()

		# audio.add_picture(image)
		# audio.save()
		# import pdb
		# pdb.set_trace()
		audio = MP3(song, ID3=ID3)
		# import pdb
		# pdb.set_trace()
		audio.tags.add(
		    APIC(
		        encoding=3, # 3 is for utf-8
		        mime='image/jpg', # image/jpeg or image/png
		        type=3, # 3 is for the cover image
		        desc=u'Cover',
		        data=open(options[3], 'rb').read()
		    )
		)
	audio.save()
	

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
		# import pdb
		# pdb.set_trace()
		for i in range(0, list_len):
			curr_num = option_list[i]
			if curr_num.isdigit(): 
				if i < list_len-2 and option_list[i+1].isalpha():
					to_return.append(curr_num + 'e')
				else:
					to_return.append(curr_num)
			elif curr_num == '-':
				to_return.append(curr_num)
	else:
		to_return = option_list
	# if option_list[list_len-1] is '-':
	# 	to_return.append('-')
	
	return to_return

def edit_prop(thing_to_edit):
	print 'You chose to edit `' + thing_to_edit + '`'
	to_return = raw_input('What should it be? ')
	return to_return

def get_data(options, data):
	title = None
	artist = None
	album = '-'
	local_art = '-'
	for i in range(0, 4):
		option = options[i]
		edit = False
		if len(option) > 1:
			edit = True
			option = option[0]
		if option == '-':
			continue
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
			use = ''
			if data_to_use['local_art'] is not None:
				use = data_to_use['local_art']
			local_art = use
	to_return = [title, artist, album, local_art]
	if len(options) is 5:
		to_return.append('-')
	return to_return







