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

    def __init__(self, page):
        self.page = page


class LiveLeaderboards(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.scores.LiveLeaderboards`
    """
    __selections = {
        "player_type": {"css_selector": ".playertypes"},
        "positions": {"css_selector": ".positions"},
        "stat_type": {"css_selector": ".stattypes"}
    }

    def __init__(self, page):
        super().__init__(page)


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


class BoxScore:
    """
    CSS selectors for :py:class:`fangraphs.scores.BoxScore`
    """
    __dropdowns_type_1 = {
        "season": (
            "#WinsBox1_rcbSeason",
            "#WinsBox1_rcbSeason_DropDown"
        ),
        "team": (
            "#WinsBox1_cbTeams",
            "#WinsBox1_cbTeams_DropDown"
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
        #     self.__setattr__(key, selectors.Calendars(page, *val))
