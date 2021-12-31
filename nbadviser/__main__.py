"""Main script entry point"""

from nbadviser import bot
from nbadviser import config
from nbadviser.config import logger


def main():
    logger.info('Старт NBAdviser')
    bot.run(token=config.TOKEN)


if __name__ == '__main__':
    main()
