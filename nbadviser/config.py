"""File with service settings
"""

import os
import platform
from loguru import logger


def configure_log_filename():
    """Determine log filename and create a directory if needed"""
    log_filename = 'nbadviser.log'

    if platform.system() == 'Windows':
        log_path = 'C:\\logs\\'
        if not os.path.exists(log_path):
            os.mkdir(log_path)
    else:
        log_path = ''  # fixme
    return log_path + log_filename


TOKEN = os.environ['NBADVISER_TOKEN']
CONTROL_CHAT_ID = os.environ['NBADVISER_CONTROL_CHAT_ID']

LOG_FILENAME = configure_log_filename()
LOG_LEVEL = 'INFO'
LOG_ROTATION = '1 week'
LOR_RETENTION = '1 month'
logger.add(sink=LOG_FILENAME, level=LOG_LEVEL, rotation=LOG_ROTATION,
           retention=LOR_RETENTION)
