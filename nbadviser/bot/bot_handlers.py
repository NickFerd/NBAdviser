"""Callback function for bot handlers"""
import traceback

from telegram import Update, ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from nbadviser import adviser, config
from nbadviser.config import logger
from nbadviser.logics.adviser import Errors

BUTTON = "Топ матчи игрового дня 🏀"


def start(update: Update, context: CallbackContext):
    """Entry point to menu"""
    keyboard = [
        [BUTTON]
    ]
    message = 'Подберу интересные матчи прошедшего игрового дня, ' \
              'не раскрывая счета!\n' \
              'Нажми на кнопку ниже или введи команду /top'
    update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True,
                                         resize_keyboard=True)
    )


def get_recommendations(update: Update, context: CallbackContext) -> None:
    """Handler for making recommendations"""

    msg = update.message.reply_text(
        f'Идет отбор игр...'
    )

    recommendations, errors = adviser.get_recommendations()
    handle_strategies_errors(context, errors)

    msg.edit_text(recommendations.to_html(), parse_mode=ParseMode.HTML)


def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors, that happen outside of executing strategies"""
    tb = traceback.format_tb(context.error.__traceback__)
    tb = ''.join(tb)

    msg = f'<u>BOT ERROR</u>:\n' \
          f'Error: {context.error}\n'

    # Send notification to control chat
    if config.SEND_ON_ERROR:
        context.bot.send_message(chat_id=config.CONTROL_CHAT_ID, text=msg,
                                 parse_mode=ParseMode.HTML)

    # Add traceback and log
    msg += f"Traceback (most recent call last):\n" \
           f"{tb}"
    logger.error(msg)


def handle_strategies_errors(context: CallbackContext,
                             errors: Errors) -> None:
    """Handle errors that occur during execution of strategies"""
    for error in errors:
        msg = f"<u>STRATEGY ERROR</u>\n"
        msg += f"Strategy: {error.label}\n" \
               f"Exception: {error.exception}\n"

        # Send notification to control chat
        if config.SEND_ON_ERROR:
            context.bot.send_message(chat_id=config.CONTROL_CHAT_ID, text=msg,
                                     parse_mode=ParseMode.HTML)

        # Add traceback and log
        msg += f"{error.traceback}"
        logger.error(msg)
