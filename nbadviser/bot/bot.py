"""Telegram bot entry point"""

from telegram.ext import Updater, CommandHandler
from nbadviser.bot import bot_handlers


def run(config):
    """Initializing of tg bot"""

    updater = Updater(token=config.TOKEN)
    dispatcher = updater.dispatcher

    # Adding handlers
    dispatcher.add_handler(CommandHandler('run',
                                          bot_handlers.get_recommendations))

    # Starting Bot
    updater.start_polling()

    # Cleanup
    updater.idle()

