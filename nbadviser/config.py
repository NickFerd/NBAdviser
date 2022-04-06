"""File with service settings
"""

import os
import platform
import pytz
from loguru import logger


def configure_log_filename():
    """Determine log filename and create a directory if needed"""
    log_filename = 'nbadviser.log'

    if platform.system() == 'Windows':
        log_path = 'C:\\logs\\'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
    else:
        log_path = '/var/log/nbadviser/'
    return log_path + log_filename


# Environment
TOKEN = os.environ.get('NBADVISER_TOKEN')
try:
    CONTROL_CHAT_ID = os.environ['NBADVISER_CONTROL_CHAT_ID']
except KeyError:
    SEND_ON_ERROR = False
else:
    SEND_ON_ERROR = True

# Logging
LOG_FILENAME = configure_log_filename()
LOG_LEVEL = 'INFO'
LOG_ROTATION = '1 month'
logger.add(sink=LOG_FILENAME, level=LOG_LEVEL, rotation=LOG_ROTATION,
           encoding='utf8')

ETC_TIMEZONE = pytz.timezone('US/Eastern')

LINK_FULL_GAMES = 'https://nbareplay.net/'
LINK_STREAMS = 'http://6streams.tv/'
