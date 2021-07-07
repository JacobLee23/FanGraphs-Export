#! usr/bin/env python
# fangraphs/selectors/_teams.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.teams`.
"""

from . import widgets


class Summary(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.Summary`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "div.team-select-change > select.select-change-team"
        },
        "position_players": {
            "root_selector": "div.depth-chart-select > div:nth-child(2) > select"
        },
        "pitchers": {
            "root_selector": "div.depth-chart-select > div:nth-child(3) > select"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class Stats(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.Stats`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "div.team-select-change > select.select-change-team"
        },
        "team_select": {
            "root_selector": ".team-stats-select-team > select"
        },
        "select_season": {
            "root_selector": ".team-stats-select-year > select"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class Schedule(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.Schedule`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "div.team-select-change > select.select-change-team"
        },
        "select_season": {
            "root_selector": "div.team-schedule-select-year > select"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class PlayerUsage(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.PlayerUsage`.
    """
    _selections = {
        "mode": {
            "root_selector": "#root-team-lineup > div > div:nth-child(1)"
        },
        "handedness": {
            "root_selector": "#root-team-lineup > div > div:nth-child(2)"
        }
    }
    _dropdowns = {
        "team": {
            "root_selector": "div.team-select-change > select.select-change-team"
        },
        "season": {
            "root_selector": "#root-team-lineup > div > div:nth-child(3)"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class DepthChart(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.DepthChart`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "div.team-select-change > select.select-change-team"
        },
        "position_players": {
            "root_selector": "div.depth-chart-select > div:nth-child(2) > select"
        },
        "pitchers": {
            "root_selector": "div.depth-chart-select > div:nth-child(3) > select"
        }
    }

    def __init__(self, page):
        super().__init__(page)
