import logging

def get_logger(name):
	logger = logging.getLogger(name)

	logger.setLevel(logging.DEBUG)

	handler = logging.FileHandler('./hello.log')
	handler.setLevel(logging.DEBUG)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	logger.addHandler(handler)
	return logger