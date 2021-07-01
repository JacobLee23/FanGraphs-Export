#! python3
# fangraphs/selectors/dcharts_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.teams`.
"""

from fangraphs import selectors


class Summary(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.Summary`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "select.select-change-team"
        },
        "position_players": {
            "root_selector": ".select-container:nth-child(1) > select.pos-stat"
        },
        "pitchers": {
            "root_selector": ".select-container:nth-child(2) > select.pos-stat"
        }
    }

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "position_players": ".select-container:nth-child(1) > select.pos-stat",
        "pitchers": ".select-container:nth-child(2) > select.pos-stat"
    }

    def __init__(self, page):
        super().__init__(page)


class Stats(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.Stats`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "select.select-change-team"
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


class Schedule(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.Schedule`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "select.select-change-team"
        },
        "select_season": {
            "root_selector": ".team-stats-select-year > select"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class PlayerUsage(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.PlayerUsage`.
    """
    _selections = {
        "mode": {
            "root_selector": "#root-team-lineup div:nth-child(1)"
        },
        "handedness": {
            "root_selector": "#root-team-lineup div:nth-child(2)"
        }
    }
    _dropdowns = {
        "team": {
            "root_selector": "select.select-change-team"
        },
        "season": {
            "root_selector": "#root-team-lineup div:nth-child(3)"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class DepthChart(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.DepthChart`.
    """
    _dropdowns = {
        "team": {
            "root_selector": "select.select-change-team"
        },
        "position_players": {
            "root_selector": ".select-container:nth-child(1) > select.pos-stat"
        },
        "pitchers": {
            "root_selector": ".select-container:nth-child(2) > select.pos-stat"
        }
    }

    def __init__(self, page):
        super().__init__(page)
