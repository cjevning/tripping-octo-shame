import datetime as dt
import os
import ConfigParser

necessary_dirs = ['./songs', './art_dump', './html_pages']

if __name__ == "__main__":
	for ndir in necessary_dirs:
		if not os.path.exists(ndir):
			os.makedirs(ndir)
	sdir = raw_input('enter directory where music files will be saved:')
	allow = raw_input('retry and allow qualtiy exceptions if mp3 not found? y or n:')
	if allow.lower() in ['y', 'yes', 'true']:
		retry_with_quality_exceptions = True
	else:
		retry_with_quality_exceptions = False
	config = ConfigParser.RawConfigParser()
	section = 'defaults'
	config.add_section(section)
	config.set(section, 'rwqe', str(retry_with_quality_exceptions))
	config.set(section, 'directory', sdir.rstrip('/'))
	config.set(section, 'root', os.getcwd())
	with open('./defaults.cfg', 'wb') as configfile:
		config.write(configfile)
	
