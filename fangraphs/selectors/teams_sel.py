#! python3
# fangraphs/selectors/dcharts_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.teams`.
"""

from fangraphs import selectors


class Summary:
    """
    CSS selectors for :py:class:`fangraphs.teams.Summary`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "position_players": ".select-container:nth-child(1) > select.pos-stat",
        "pitchers": ".select-container:nth-child(2) > select.pos-stat"
    }
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))


class Stats:
    """
    CSS selectors for :py:class:`fangraphs.teams.Stats`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "team_select": ".team-stats-select-team > select",
        "select_season": ".team-stats-select-year > select"
    }
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))


class Schedule:
    """
    CSS selectors for :py:class:`fangraphs.teams.Schedule`.
    """

    __dropdowns_type_4 = {
        "team": "select.select-change-team",
        "select_season": ".team-schedule-select-year > select"
    }
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__dropdowns_type_4.items():
            self.__setattr__(key, selectors.DropdownsType4(page, val))