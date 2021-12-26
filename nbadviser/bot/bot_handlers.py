"""Callback function for bot handlers"""

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from nbadviser import adviser


def get_recommendations(update: Update, context: CallbackContext):
    """Handler for making recommendations"""
    msg = update.message.reply_text(
        f'Подбираю интересные игры прошедшего игрового дня...🏀')
    recommendations, errors = adviser.get_recommendations()
    # msg.edit_text('Подборка интересный игр прошедшего игрового дня')
    update.message.reply_text(recommendations.to_html(),
                              parse_mode=ParseMode.HTML)
