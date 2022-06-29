"""Telegram bot entry point"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from nbadviser.bot import bot_handlers
from nbadviser.bot.bot_handlers import error_handler


def run(token: str):
    """Initializing of tg bot"""

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', bot_handlers.start))
    dispatcher.add_handler(
        MessageHandler(Filters.regex(f'^{bot_handlers.TOP_GAMES_BUTTON}$'),
                       bot_handlers.get_recommendations)
    )
    dispatcher.add_handler(
        CommandHandler('top', bot_handlers.get_recommendations)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(f'^{bot_handlers.HELP_BUTTON}'),
                       bot_handlers.help_handler)
    )
    dispatcher.add_handler(
        CommandHandler('help', bot_handlers.help_handler)
    )
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()
