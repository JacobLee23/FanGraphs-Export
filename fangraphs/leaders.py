#! usr/bin/env python
# fangraphs/leaders.py

"""
Scrapers for the webpages under the FanGaphs **Leaders** tab.
"""

from typing import *

import pandas as pd

import fangraphs.exceptions
from fangraphs import FilterWidgets
from fangraphs.selectors import leaders_


class GameSpan(FilterWidgets):
    """
    Scraper for the FanGraphs `60-Game Span Leaderboards`_ page.

    .. _60-Game Span Leaderboards: https://www.fangraphs.com/leaders/special/60-game-span
    """
    _widget_class = leaders_.GameSpan
    address = "https://fangraphs.com/leaders/special/60-game-span"

    def __init__(self, **kwargs):
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        :return:
        """
        dataframe = self.export_data()
        self._data = dataframe


class International(FilterWidgets):
    """
    Scraper for the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """
    _widget_class = leaders_.International
    address = "https://www.fangraphs.com/leaders/international"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        :return:
        """
        dataframe = self.export_data()
        self._data = dataframe


class MajorLeague(FilterWidgets):
    """
    Scraper for the FanGraphs `Major League Leaderboards`_ page.

    *Note: The Splits Leaderboards are covered by :py:class:`SplitsLeaderboards`.*

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """
    _widget_class = leaders_.MajorLeague
    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        :return:
        """
        dataframe = self.export_data()
        self._data = dataframe


class SeasonStat(FilterWidgets):
    """
    Scraper for the FanGraphs `Season Stat Grid`_ page.

    .. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
    """
    _widget_class = leaders_.SeasonStat
    address = "https://fangraphs.com/leaders/season-stat-grid"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, table_size="Infinity", **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        :return:
        """
        table = self.soup.select_one(".table-scroll")
        table_data = self.scrape_table(table)

        df = table_data.dataframe.copy()
        df.drop(columns=df.columns[0])

        self._data = df


class Splits(FilterWidgets):
    """
    Scraper for the FanGraphs `Splits Leaderboards`_ page.

    .. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
    """
    _widget_class = leaders_.Splits
    address = "https://fangraphs.com/leaders/splits-leaderboards"

    qsbatting = leaders_.QSBatting()
    qspitching = leaders_.QSPitching()

    def __init__(
            self, *,
            batting_qs: Optional[str] = None,
            pitching_qs: Optional[str] = None,
            filter_group: str = "Show All",
            **kwargs
    ):
        """
        :param batting_qs:
        :param pitching_qs:
        """
        assert not (batting_qs and pitching_qs)
        if batting_qs:
            assert batting_qs in self.qsbatting.__dict__["options"].values()
            quick_configure = batting_qs
        elif pitching_qs:
            assert pitching_qs in self.qspitching.__dict__["options"].values()
            quick_configure = pitching_qs
        else:
            quick_configure = None

        self.filter_groups = None
        expand_menu = self._get_filter_group(filter_group)

        FilterWidgets.__init__(
            self,
            expand_menu=expand_menu,
            quick_configure=quick_configure,
            submit_form="#button-update",
            **kwargs
        )

        self.data = None

    @property
    def filter_groups(self) -> list[str]:
        """

        :return:
        """
        return self._filter_groups

    @filter_groups.setter
    def filter_groups(self, value) -> None:
        """

        """
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        options = [e.text for e in elems]
        self._filter_groups = options

    def _get_filter_group(self, group: str) -> str:
        """

        :param group:
        :return:
        """
        options = [o.lower() for o in self.filter_groups]
        try:
            index = options.index(group)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterGroup(group) from err

        css = f"div.fgBin.splits-bin-controller > div.fgButton:nth-child({index+1})"
        return css

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        """
        dataframe = self.export_data()
        self._data = dataframe


class WAR(FilterWidgets):
    """
    Scraper for the FanGraphs `Combined WAR Leaderboards`_ page.

    .. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
    """
    _widget_class = leaders_.WAR
    address = "https://fangraphs.com/warleaders.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        :return:
        """
        dataframe = self.export_data()
        self._data = dataframe
