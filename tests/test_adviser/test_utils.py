"""Tests for helping classes and functions from adviser/utils.py"""

from nbadviser.adviser.utils import Team, Teams


def test_teams_access_by_id():
    """Check proper work of get_by_id function of class Teams"""
    team_1 = Team(team_id=1)
    team_2 = Team(team_id=2)
    teams = Teams(home=team_1, visitor=team_2)
    assert teams.get_by_id(team_id=1) is team_1
    assert teams.get_by_id(team_id=2) is team_2
