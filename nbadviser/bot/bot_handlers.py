"""Callback function for bot handlers"""

import traceback

from telegram import Update, ParseMode, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from nbadviser import adviser, config
from nbadviser.adviser.adviser import Errors
from nbadviser.bot.utils import check_format, access_log
from nbadviser.config import logger, LINK_FULL_GAMES, LINK_STREAMS

BUTTON = "Топовые матчи игрового дня 🏀"
HELP_BUTTON = "Помощь"


@access_log
def start(update: Update, context: CallbackContext):
    """Entry point to menu"""
    keyboard = [
        [BUTTON],
        [HELP_BUTTON]
    ]
    message = 'Подберу интересные матчи прошедшего игрового дня, ' \
              'не раскрывая счета!\n' \
              'Нажми на кнопку ниже или введи команду /top'
    update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True,
                                         resize_keyboard=True)
    )


@access_log
def help_handler(update: Update, context: CallbackContext):
    """Help button and command /help handler"""

    msg = '<b>NBAdviser</b> - бот, который поможет ' \
          'тебе выбрать интересную игру\n\n' \
          '<b>/top</b> - рекомендации за последний игровой день\n' \
          '<b>/top 2022-01-12</b>  - за конкретный день\n\n' \
          'Обратная связь: https://t.me/NickFerd'

    update.message.reply_text(msg, parse_mode=ParseMode.HTML,
                              disable_web_page_preview=True)


@access_log
def get_recommendations(update: Update, context: CallbackContext) -> None:
    """Handler for making recommendations"""

    msg = update.message.reply_text(
        f'Идет отбор игр...'
    )

    games_date = None
    if context.args:
        games_date_unchecked = context.args[0]  # Always look at first argument
        if check_format(games_date_unchecked):
            games_date = games_date_unchecked

    # Set additional parameters
    adviser.set_parameters(games_date=games_date)

    recommendations, errors = adviser.get_recommendations()
    handle_strategies_errors(context, errors)

    additional_text = f'\n<i>Ссылка для просмотра полных матчей</i>:' \
                      f'\n{LINK_FULL_GAMES}'
    msg.edit_text(recommendations.to_html() + additional_text,
                  parse_mode=ParseMode.HTML,
                  disable_web_page_preview=True)

    # Additionally check for live games if user required last game day
    # and send results (if any) in separate message
    if not games_date:
        live_games_recommendation = adviser.get_live_games_or_none()
        if live_games_recommendation:
            header = '<i>Может быть интересно:</i>\n'
            footer = f'\n<i>Ссылка со стримами в хорошем качестве</i>:' \
                     f'\n{LINK_STREAMS}'
            message = header + live_games_recommendation.to_html() + footer
            update.message.reply_text(message,
                                      parse_mode=ParseMode.HTML,
                                      disable_web_page_preview=True)


def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors, that happen outside of executing strategies"""

    # Message to client
    update.message.reply_text("К сожалению, произошла ошибка.")

    # Logging and alerting control chat
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
