"""Наброски
Пробы использования библиотек.
"""
from pprint import pprint

from operator import attrgetter

import requests
import m3u8
import m3u8_To_MP4
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.endpoints import leaguegamelog, leaguegamefinder, \
    scoreboardv2, LeagueDashTeamClutch
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
    # games_log = leaguegamelog.LeagueGameLog(date_from_nullable='2022-01-03')
    # games = games_log.league_game_log.get_dict()
    # print(games['headers'])
    # pprint(games)

    # scoreboard_for_yesterday = scoreboardv2.ScoreboardV2(
    # game_date='2022-01-03')
    # print(dir(scoreboard_for_yesterday))
    # pprint(scoreboard_for_yesterday.get_dict(), indent=1)
    league_clutch = LeagueDashTeamClutch(
        date_from_nullable='2022-01-03'
    )
    print(dir(league_clutch))
    pprint(league_clutch.league_dash_team_clutch.get_dict())
    pprint(league_clutch.team_stats.get_dict())
    # score = scoreboard_for_yesterday.available.get_dict()
    # pprint(score)
    # scores = scoreboard_for_yesterday.line_score.get_dict()
    # games_status = scoreboard_for_yesterday.game_header.get_dict()
    # pprint(games_status)
    # game = scores['data'][0]
    # print('All games - ', len(scores['data']))
    # headers = scores['headers']
    # matches = {}
    # for header, value in zip(headers, game):
    #     print(header, value)


def timezones():
    import datetime
    import pytz

    etc = pytz.timezone('US/Eastern')
    print(etc)
    naive_dt = datetime.datetime.now()
    print(naive_dt)
    now_est = naive_dt.astimezone(etc)
    print(now_est)
    print(str(now_est))
    print(now_est.date())
    noe_est_date = now_est.date()
    print(str(noe_est_date))
    print(type(str(noe_est_date)))


def video_highlights():
    url = 'https://content-api-prod.nba.com/public/1/content/video/?games' \
          '=0022000001&status=publish&meta-video_creation_source=wsc-feed'

    params = {'games': '0022000001',
              'status': 'publish',
              'meta-video_creation_source': 'wsc-feed'}

    result = requests.get(url=url, params=params)
    result = result.json()

    pprint(result)


def m3u8_converter():
    # playlist = m3u8.load(
    #     'https://nbanlds19vod.akamaized.net/nlds_vod/nba/vod/2020/12/22'
    #     '/69f6d540-0523-3de6-2f9a-ac837f000001/v1/stream/69f6d540-0523-3de6'
    #     '-2f9a-ac837f000001_1_pc.mp4.m3u8')

    # print(dir(playlist))
    # print(playlist.segments)
    # print(playlist.data)
    # print(playlist.playlist_type)
    # url = 'https://nbanlds19vod.akamaized.net/nlds_vod/nba/vod/2020/12/22/f8e0e270-0503-3de6-6d9f-4aac7f000001/v1/stream/f8e0e270-0503-3de6-6d9f-4aac7f000001_1_pc.mp4.m3u8'
    # m3u8_To_MP4.async_download(url)


    # video_url = """https://nbanlds19vod.akamaized.net/nlds_vod/nba/vod/2022/02/12/205c3e80-4c16-3de7-3785-08f67f000001/v2/stream/205c3e80-4c16-3de7-3785-08f67f000001_2_pc.mp4.m3u8"""
    video_url = """https://nbanlds19vod.akamaized.net/nlds_vod/nba/vod/2022/02/12/205c3e80-4c16-3de7-3785-08f67f000001/v2/stream/205c3e80-4c16-3de7-3785-08f67f000001_2_1600/205c3e80-4c16-3de7-3785-08f67f000001_2_1600_000130023267.ts"""

    playlist_1 = m3u8.load(video_url)
    pprint(playlist_1.data)
    # for segment in playlist_1.segments:
    #     attrs = dir(segment)
        # for attr in attrs:
        #     if not attr.startswith('__'):
        #         pprint(attr)
        #         value = attrgetter(attr, segment)
        #         pprint(value)

    print(playlist_1.target_duration)

    """https://russianblogs.com/article/3732606495/"""


def alternative_data_providers():
    # ESPN API (нужно изучать на предмет применимости)
    # Found on the web
    "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401360704"  # Game_id
    "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    "https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b"

    # Rapid API (paid and not flexible)
    import requests

    # url = "https://api-nba-v1.p.rapidapi.com/games/date/%7B2022-02-16%7D"
    #
    # headers = {
    #     'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
    #     'x-rapidapi-key': "bd100a84demsh059fe5562cef2b9p11d7d0jsne52b761fbaec"
    # }
    #
    # response = requests.request("GET", url, headers=headers)
    #
    # pprint(response.text)

    # Sportsdata.io (paid I guess, but interesting endpoints)
    url = 'https://api.sportsdata.io/v3/nba/scores/json/AreAnyGamesInProgress'
    response = requests.get(url)
    pprint(response.json())


if __name__ == '__main__':
    alternative_data_providers()
    # video_highlights()
    # m3u8_converter()
    # main()
    # nba_api()
    # timezones()
