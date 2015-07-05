import urllib2
import logger_setup as ls
logger = ls.get_logger(__name__)

def download_file(link, file_path):
	try:
		url = urllib2.urlopen(link)
		f = open(file_path, 'wb')
		splitfile = file_path.split('/')
		filename = splitfile[len(splitfile)-1]
		meta = url.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		logger.info("Downloading: %s Bytes: %s" % ("'" + filename + "'", file_size))

		file_size_dl = 0
		block_sz = 8192
		tracker = 0
		while True:
		    buffer = url.read(block_sz)
		    if not buffer:
		        break

		    file_size_dl += len(buffer)
		    f.write(buffer)
		    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		    status = status + chr(8)*(len(status)+1)
		    progess = int(status[status.rfind('[')+1:status.rfind('.', )])
		    if progess % 10 == 0 and progess/10 == tracker:
		    	logger.info(status)
		    	tracker += 1

		f.close()
		logger.info('download successful!')
		return True
	except Exception,e:
		logger.error( "file found but download failed for this reason:")
		logger.error(e)
		return False


if __name__ == "__main__":
	import sys
	download_file(sys.argv[1], sys.argv[2])