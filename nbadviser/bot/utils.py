"""Helping functions for bot"""
import time
from datetime import datetime

import functools
from typing import Callable

from nbadviser.config import logger


def check_format(games_date: str):
    """Check that given string in format of YYYY-MM-DD"""
    try:
        datetime.strptime(games_date, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True


def access_log(handler: Callable):
    """Decorator for logging a bot handler call
    Intended to be used with python-telegram-bot handlers that take Update and
    CallbackContext objects as positional arguments"""

    @functools.wraps(handler)
    def wrapper(update, context):
        """Wrapper"""
        user = f'full_name={update.message.from_user.full_name}, ' \
               f'username={update.message.from_user.username}, ' \
               f'id={update.message.from_user.id}'
        command = f'{update.message.text}'

        start_time = time.time()
        handler(update, context)
        finish_time = time.time()
        logger.info(f'User: {user}|Command: {command}|'
                    f'Execution time: {finish_time-start_time:.3f}')

    return wrapper

