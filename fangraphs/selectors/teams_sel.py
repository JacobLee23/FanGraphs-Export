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

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "position_players": ".select-container:nth-child(1) > select.pos-stat",
        "pitchers": ".select-container:nth-child(2) > select.pos-stat"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))


class Stats(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.Stats`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "team_select": ".team-stats-select-team > select",
        "select_season": ".team-stats-select-year > select"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))


class Schedule(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.Schedule`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "select_season": ".team-schedule-select-year > select"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))


class PlayerUsage(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.PlayerUsage`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team"
    }
    __dropdowns_type_3 = {
        "season": "#root-team-lineup div:nth-child(3)"
    }
    __selections_type_3 = {
        "mode": "#root-team-lineup div:nth-child(1)",
        "handedness": "#root-team-lineup div:nth-child(2)"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))
        for key, val in self.__dropdowns_type_3.items():
            self.__setattr__(key, selectors.DropdownsType3(page, val))


class DepthChart(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.teams.DepthChart`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "position_players": ".select-container:nth-child(1) > select.pos-stat",
        "pitchers": ".select-container:nth-child(2) > select.pos-stat"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))
