"""Tests for helping classes and functions from adviser/utils.py"""

from freezegun import freeze_time

from nbadviser.adviser.utils import Team, Teams, get_date_etc_str


def test_teams_access_by_id():
    """Check proper work of get_by_id function of class Teams"""
    team_1 = Team(team_id=1)
    team_2 = Team(team_id=2)
    teams = Teams(home=team_1, visitor=team_2)
    assert teams.get_by_id(team_id=1) is team_1
    assert teams.get_by_id(team_id=2) is team_2


def test_get_date_est_str():
    """Check proper work of function get_date_est_str()"""

    with freeze_time('2022-03-28 18:00:00', tz_offset=4):
        ref = '2022-03-27'
        res = get_date_etc_str()
        assert res == ref

    with freeze_time('2022-03-28 23:30:00', tz_offset=4):
        ref = '2022-03-28'
        res = get_date_etc_str()
        assert res == ref
