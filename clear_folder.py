import os

def clear(folder_path):
	folder = folder_path
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception, e:
	        import logger_setup as ls
	        logger = ls.get_logger(__name__)
	        logger.error('unable to clear directory:')
	        logger.error(e)

if __name__ == '__main__':
	import sys
	clear(sys.argv[1])