from mutagen.easyid3 import EasyID3
import sys
import os
from mutagen.mp3 import MP3
import mutagen
from mutagen.id3 import ID3, ID3NoHeaderError

if __name__ == "__main__":
	if len(sys.argv) > 1:
		directory = raw_input('what directory do you want to edit the tags of?')
		tag = raw_input('which tag do you want to edit?')
		edit = raw_input('what should it be?')
		for root, dirs, files in os.walk(directory):
			# import pdb
			# pdb.set_trace()
			for file in files:
				if file.endswith(".mp3"):
					try:
						meta = EasyID3(root + '\\' + file)
						meta[tag] = edit
						meta.save()
					except:
						continue
	else:
		filename = raw_input('what file do you want to edit the tags of?')
		tag = raw_input('which tag do you want to edit?')
		edit = raw_input('what should it be?')
		try:
			meta = EasyID3(filename)
		except ID3NoHeaderError:
			meta = mutagen.File(filename, easy=True)
			meta.add_tags()
		meta[tag] = edit
		meta.save()

def reset_tags(song):
	meta = mutagen.File(song, easy=True)
	meta.add_tags()
	meta.save()