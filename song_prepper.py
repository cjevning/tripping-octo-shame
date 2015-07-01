import sys

def parse_file(file_path):
	to_return = []
	with open(file_path) as myFile:
		for line in myFile:
			x = line.rstrip()
			to_return.append(x)
	myFile.close()
	return to_return

def read_command():
	num_args = len(sys.argv)

	if num_args <= 1:
		print "you need to specify either a file name or a song"

	songs = []
	start_of_non_flags = 1
	flag = sys.argv[1]
	if flag.startswith('-allow'):
		allow_quality_exceptions = True
		start_of_non_flags = 2
	potential_file_name = sys.argv[start_of_non_flags]
	if potential_file_name.endswith('.txt'):
		print 'text file with songs found, parsing'
		songs = parse_file(potential_file_name)
	else:
		print 'no text file given, treating args as song title'
		songs.append(' '.join(sys.argv[start_of_non_flags:]))
	return songs