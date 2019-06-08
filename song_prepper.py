import sys
import logger_setup as ls
logger = ls.get_logger(__name__)

def parse_file(file_path):
	to_return = []
	with open(file_path) as myFile:
		for line in myFile:
			x = line.rstrip()
			to_return.append(x)
	myFile.close()
	return to_return

def read_command(path = None):
	if path is not None:
		songs = parse_file(path)
	else:
		num_args = len(sys.argv)
		if num_args <= 1:
			print "you need to specify either a file name or a song"

		songs = []
		potential_file_name = sys.argv[1]
		if potential_file_name.endswith('.txt'):
			logger.info('text file with songs found, parsing')
			songs = parse_file(potential_file_name)
		else:
			logger.info('no text file given, treating args as song title')
			songs.append(' '.join(sys.argv[1:]))
	return songs
