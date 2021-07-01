#! usr/bin/env python
# fangraphs/selectors/_scores.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.leaders`.
"""

from . import widgets


class Live(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.Live`
    """

    def __init__(self, page):
        super().__init__(page)


class LiveLeaderboards(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.LiveLeaderboards`
    """
    __selections = {
        "player_type": {"root_selector": ".playertypes"},
        "positions": {"root_selector": ".positions"},
        "stat_type": {"root_selector": ".stattypes"}
    }

    def __init__(self, page):
        super().__init__(page)


class Scoreboard(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.Scoreboard`
    """
    _dropdowns = {
        "season": {
            "root_selector": "#LiveBoard1_rcbSeason",
            "dropdown_selector": "#LiveBoard1_rcbSeason_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class GameGraphs(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.GameGraphs`
    """
    _dropdowns = {
        "season": {
            "root_selector": "#WinsGame1_rcbSeason",
            "dropdown_selector": "#WinsGame1_rcbSeason_DropDown"
        },
        "team": {
            "root_selector": "#WinsGame1_cbTeams",
            "dropdown_selector": "#WinsGame1_cbTeams_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class PlayLog(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.PlayLog`
    """
    _dropdowns = {
        "season": {
            "root_selector": "#PlayGame1_rcbSeason",
            "dropdown_selector": "#PlayGame1_rcbSeason_DropDown"
        },
        "team": {
            "root_selector": "#PlayGame1_cbTeams",
            "dropdown_selector": "#PlayGame1_cbTeams_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class BoxScore(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.scores.BoxScore`
    """
    _dropdowns = {
        "season": {
            "root_selector": "#WinsBox1_rcbSeason",
            "dropdown_selector": "#WinsBox1_rcbSeason_DropDown"
        },
        "team": {
            "root_selector": "#WinsBox1_cbTeams",
            "dropdown_selector": "#WinsBox1_cbTeams_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)
