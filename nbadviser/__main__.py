"""Main script entry point"""

from nbadviser import bot
from nbadviser import config


def main():
    bot.run(token=config.TOKEN)


if __name__ == '__main__':
    main()
