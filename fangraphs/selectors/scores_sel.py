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
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        self.page = page


class LiveLeaderboards:
    """
    CSS selectors for :py:class:`fangraphs.leaders.LiveLeaderboards`.
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
