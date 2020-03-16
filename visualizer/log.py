import logging

# set up logging
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(log_color)s[%(asctime)s] %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
from colorlog import ColoredFormatter
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT,log_colors={
		'DEBUG':    'cyan',
		'INFO':     'green',
		'WARNING':  'yellow',
		'ERROR':    'red',
		'CRITICAL': 'red,bg_white',
	},datefmt='%Y-%m-%d %H:%M:%S')
with open("positions.log", "w"): pass
fh = logging.FileHandler('positions.log')
fh.setLevel(LOG_LEVEL)
fh.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(fh)