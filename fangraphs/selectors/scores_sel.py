#! python3
# fangraphs/selectors/leaders_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.leaders`.
"""

from fangraphs import selectors


class Live:
    """
    CSS selectors for :py:class:`fangraphs.scores.Live`
    """
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        self.page = page


class LiveLeaderboards:
    """
    CSS selectors for :py:class:`fangraphs.scores.LiveLeaderboards`
    """
    __selections_type_4 = {
        "player_type": ".playertypes",
        "positions": ".positions",
        "stat_type": ".stattypes"
    }

    waitfor = ".fg-data-grid.undefined"
    export_data = ""

    def __init__(self, page):
        for key, val in self.__selections_type_4.items():
            self.__setattr__(key, selectors.SelectionsType4(page, val))


class Scoreboard:
    """
    CSS selectors for :py:class:`fangraphs.scores.Scoreboard`
    """
    __calendars = {
        "date": (
            "#LiveBoard1_rdpDate_popupButton",
            "#LiveBoard1_rdpDate_calendar",
            "#LiveBoard1_rdpDate_dateInput_wrapper"
        )
    }
    __dropdowns_type_1 = {
        "season": (
            "#LiveBoard1_rcbSeason",
            "#LiveBoard1_rcbSeason_DropDown"
        )
    }

    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__calendars.items():
            self.__setattr__(key, selectors.Calendars(page, *val))


class GameGraphs:
    """
    CSS selectors for :py:class:`fangraphs.scores.GameGraphs`
    """
    __dropdowns_type_1 = {
        "season": (
            "#WinsGame1_rcbSeason",
            "#WinsGame1_rcbSeason_DropDown"
        ),
        "team": (
            "#WinsGame1_cbTeams",
            "#WinsGame1_cbTeams_DropDown"
        )
    }
    __calendars = {
        "date": ()
    }
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
        # for key, val in self.__calendars.items():
        #    self.__setattr__(key, selectors.Calendars(page, *val))


class PlayLog:
    """
    CSS selectors for :py:class:`fangraphs.scores.PlayLog`
    """
    __dropdowns_type_1 = {
        "season": (
            "#PlayGame1_rcbSeason",
            "#PlayGame1_rcbSeason_DropDown"
        ),
        "team": (
            "#PlayGame1_cbTeams",
            "#PlayGame1_cbTeams_DropDown"
        )
    }
    __calendars = {
        "date": ()
    }

    waitfor = ".fg-data-grid"
    export_data = ""

    def __init__(self, page):
        for key, val in self.__dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
        # for key, val in self.__calendars.items():
        #     self.__setattr__(key, selectors.Calendars(page, *val))
