"""Callback function for bot handlers"""

from telegram import Update
from telegram.ext import CallbackContext

from nbadviser import adviser


def get_recommendations(update: Update, context: CallbackContext):
    """Handler for making recommendations"""
    games = adviser.get_recommendations()
    update.message.reply_text('I am NBAdviser and I can you give some advise!')
    update.message.reply_text(f'{games}')

