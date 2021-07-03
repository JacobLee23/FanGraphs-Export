#! usr/bin/env python
# fangraphs/leaders.py

"""
Scrapers for the webpages under the FanGaphs **Leaders** tab.
"""

import datetime
import re
from typing import *

import numpy as np
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

        def revise_dates(x, dt_format="%Y-%m-%dT%X"):
            return datetime.datetime.strptime(x, dt_format)

        dataframe["Start Date"] = dataframe["Start Date"].map(revise_dates)
        dataframe["End Date"] = dataframe["End Date"].map(revise_dates)

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

        def revise_names(x):
            regex = re.compile(r"^([A-Za-z\- ]+) ")
            if (m := regex.search(x)) is not None:
                return m.group(1)
            else:
                return x

        dataframe["Name"] = dataframe["Name"].map(revise_names)

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

    def __init__(self, *, table_size: str = "Infinity", **kwargs):
        """

        """
        FilterWidgets.__init__(self, table_size=table_size, **kwargs)

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

        dataframe = table_data.dataframe
        dataframe.drop(columns=dataframe.columns[0], inplace=True)
        dataframe.replace("", np.nan, inplace=True)

        self._data = dataframe


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
            menu_expansion: str = "Show All",
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

        FilterWidgets.__init__(
            self,
            pre_clicks=(self._widget_class.reset_css,),
            menu_expansion=menu_expansion,
            quick_configure=quick_configure,
            post_clicks=(self._widget_class.update_css,),
            **kwargs
        )

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
