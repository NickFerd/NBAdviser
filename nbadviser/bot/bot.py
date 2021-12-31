"""Telegram bot entry point"""

from telegram.ext import Updater, CommandHandler
from nbadviser.bot import bot_handlers
from nbadviser.bot.bot_handlers import error_handler


def run(token: str):
    """Initializing of tg bot"""

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # Adding handlers
    dispatcher.add_handler(CommandHandler('run',
                                          bot_handlers.get_recommendations))
    dispatcher.add_error_handler(error_handler)

    # Starting Bot
    updater.start_polling()

    # Cleanup
    updater.idle()

