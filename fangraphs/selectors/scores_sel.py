#! python3
# fangraphs/selectors/leaders_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.leaders`.
"""

from fangraphs import selectors


class Live:
    """
    CSS selectors for :py:class:`fangraphs.leaders.Live`.
    """
    __dropdowns_type_1 = {
        "season": ("#LiveBoard1_rcbSeason_Input", "#LiveBoard1_rcbSeason_DropDown")
    }
    __calendars = {
        "date": (
            "#LiveBoard1_rdpDate_popupButton",
            "#LiveBoard1_rdpDate_calendar",
            "#LiveBoard1_rdpDate_dateInput_wrapper"
        )
    }

    def __init__(self, page):
        for key, val in self.__dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
        for key, val in self.__calendars.items():
            self.__setattr__(key, selectors.Calendars(page, *val))
