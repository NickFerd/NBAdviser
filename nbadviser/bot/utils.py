"""Helping functions for bot"""

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


def log_ptb_call(handler: Callable):
    """Decorator for logging a bot handler call
    Intended to be used with python-telegram-bot handlers that take Update and
    CallbackContext objects as positional arguments"""

    @functools.wraps(handler)
    def wrapper(update, context):
        """Wrapper"""
        user = f'{update.message.from_user.username}, ' \
               f'id={update.message.from_user.id}'
        command = f'{update.message.text}'
        logger.info(f'Пользователь {user} выполнил команду: {command}')
        handler(update, context)

    return wrapper

