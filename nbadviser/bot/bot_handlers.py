"""Callback function for bot handlers"""
import traceback

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from nbadviser import adviser
from nbadviser.config import logger, CONTROL_CHAT_ID
from nbadviser.logics.adviser import Errors


def get_recommendations(update: Update, context: CallbackContext) -> None:
    """Handler for making recommendations"""
    update.message.reply_text(
        f'Подбираю интересные игры прошедшего игрового дня...🏀')
    recommendations, errors = adviser.get_recommendations()
    handle_strategies_errors(update, context, errors)
    update.message.reply_text(recommendations.to_html(),
                              parse_mode=ParseMode.HTML)


def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors, that happen outside of executing strategies"""
    tb = traceback.format_tb(context.error.__traceback__)
    tb = ''.join(tb)

    msg = f'BOT ERROR:\n' \
          f'Описание: {context.error}\n'

    # Send notification to control chat
    context.bot.send_message(chat_id=CONTROL_CHAT_ID, text=msg)

    # Add traceback and log
    msg += f"Traceback (most recent call last):\n" \
           f"{tb}"
    logger.error(msg)


def handle_strategies_errors(update: Update, context: CallbackContext,
                             errors: Errors) -> None:
    """Handle errors that occur during execution of strategies"""
    for error in errors:
        msg = f"STRATEGY ERROR:\n"
        msg += f"Strategy name: {error.label}\n" \
               f"Exception: {error.exception}\n"

        # Send notification to control chat
        context.bot.send_message(chat_id=CONTROL_CHAT_ID, text=msg)

        # Add traceback and log
        msg += f"{error.traceback}"
        logger.error(msg)
