"""Main script entry point"""

from nbadviser import bot
from nbadviser.config import Config


def main():
    config = Config()
    bot.run(config=config)


if __name__ == '__main__':
    main()
