import datetime as dt
import ConfigParser

def get_config():
	config = ConfigParser.RawConfigParser()
	config.read('./defaults.cfg')
	date = dt.date.today()
	directory = config.get('defaults', 'directory') + '/' + '.'.join([str(date.month), str(date.day), str(date.year)]) + '/'
	retry_with_quality_exceptions = config.getboolean('defaults', 'rwqe')
	root = config.get('defaults', 'root')
	songfile = config.get('defaults', 'songfile')
	return {'directory': directory, 'rwqe': retry_with_quality_exceptions, 'root': root, 'songfile':songfile}