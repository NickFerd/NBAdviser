"""Наброски
Пробы использования библиотек.
"""
from pprint import pprint

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.endpoints import leaguegamelog, leaguegamefinder
from nba_api.stats.library.parameters import GameDate

TOKEN = '5058281587:AAGzBiOx9sYke2O0S_Cx_3PhSWexkq_NTf0'


# ------ Bot sketches --------
def start(update: Update, context: CallbackContext):
    print(update)
    print(dir(context))
    update.message.reply_text('hello, it is nice to meet you')
    print(context.args)
    print(context.chat_data)
    print(context.user_data)


def main():
    """Start the bot."""
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # start bot
    updater.start_polling()

    updater.idle()


def nba_api():
    """Make nba api queries."""
    # LIVE DATA
    # board = scoreboard.ScoreBoard()
    # game_dates = board.score_board_date
    # games = board.games.get_dict()
    # print(dir(board))
    # print(game_dates)
    # pprint(games)
    # pprint(dir(games))
    # print('--------')
    #
    # box_score = boxscore.BoxScore('0022000196')
    # pprint(box_score.game.get_dict())
    # pprint(dir(box_score))

    # Games log
    games_log = leaguegamelog.LeagueGameLog(date_from_nullable='2021-12-12')
    games = games_log.league_game_log.get_dict()
    print(games['headers'])
    pprint(games)


if __name__ == '__main__':
    # main()
    nba_api()

