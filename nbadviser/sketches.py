"""Наброски
Пробы использования библиотек.
"""
from pprint import pprint

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.endpoints import leaguegamelog, leaguegamefinder, scoreboardv2
from nba_api.stats.library.parameters import GameDate


# ------ Bot sketches --------
def start(update: Update, context: CallbackContext, **kwargs):
    # handler = kwargs['handler']
    # handler.run()
    print(update)
    for el in dir(context):
        if not el.startswith('__'):
            print(el)
            print(getattr(context, el))
            print('-----')

    update.message.reply_text('hello, it is nice to meet you')


def main():
    """Start the bot."""
    # updater = Updater(token=TOKEN)
    # dispatcher = updater.dispatcher
    #
    # # handlers
    # dispatcher.add_handler(CommandHandler('start', start))
    #
    # # start bot
    # updater.start_polling()
    #
    # updater.idle()


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
    # games_log = leaguegamelog.LeagueGameLog(date_from_nullable='2021-12-12')
    # games = games_log.league_game_log.get_dict()
    # print(games['headers'])
    # pprint(games)

    scoreboard_for_yesterday = scoreboardv2.ScoreboardV2(day_offset=-1)
    print(dir(scoreboard_for_yesterday))
    pprint(scoreboard_for_yesterday.get_dict(), indent=1)
    score = scoreboard_for_yesterday.available.get_dict()
    pprint(score)
    scores = scoreboard_for_yesterday.line_score.get_dict()
    games_status = scoreboard_for_yesterday.game_header.get_dict()
    pprint(games_status)
    game = scores['data'][0]
    print('All games - ', len(scores['data']))
    headers = scores['headers']
    matches = {}
    for header, value in zip(headers, game):
        print(header, value)




if __name__ == '__main__':
    # main()
    nba_api()

