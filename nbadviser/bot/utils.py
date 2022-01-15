"""Helping functions for bot"""

from datetime import datetime


def check_format(games_date: str):
    """Check that given string in format of YYYY-MM-DD"""
    try:
        datetime.strptime(games_date, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True
