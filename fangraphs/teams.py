#! usr/bin/env python
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.

Note: The default team is the Los Angeles Angels of Anaheim.
Thus, the base URL always navigates to the stats concerning the Angels.
"""

import datetime
from typing import *

import bs4
import numpy as np
import pandas as pd

from fangraphs import PID_REGEX, PID_POS_REGEX
from fangraphs import FilterWidgets
from fangraphs.selectors import teams_


class TeamDepthChart(NamedTuple):
    p_RP: pd.DataFrame
    p_SP: pd.DataFrame

    p_C: pd.DataFrame
    p_1B: pd.DataFrame
    p_2B: pd.DataFrame
    p_3B: pd.DataFrame
    p_SS: pd.DataFrame
    p_LF: pd.DataFrame
    p_CF: pd.DataFrame
    p_RF: pd.DataFrame
    p_DH: pd.DataFrame


def scrape_depth_chart(soup: bs4.BeautifulSoup) -> TeamDepthChart:
    """

    :param soup:
    :return:
    """
    depth_chart_data = {}

    def get_player_id(elem: bs4.Tag) -> Optional[str]:
        match = PID_REGEX.search(
            elem.select_one("a").attrs.get("xlink:href")
        )
        player_id = match.group(1) if match is not None else None
        return player_id

    position_elems = (
        soup.select_one(f"g#pos{i}") for i in range(11)
    )
    for i, pos_elem in enumerate(position_elems):
        position = pos_elem.select_one(f"text#pos-label{i}").text

        player_name_elems = pos_elem.select("text.player-name")
        player_stat_elems = pos_elem.select("text.player-stat")
        player_elems = [
            (e1, e2) for (e1, e2) in zip(player_name_elems, player_stat_elems)
            if (e1.text and e2.text)
        ]
        players = [
            (e1.text, e2.text, get_player_id(e1))
            for (e1, e2) in player_elems
        ]

        dataframe = pd.DataFrame(
            data=players, columns=["Name", "Stat", "PlayerID"]
        )
        depth_chart_data.setdefault(
            f"p_{position}", dataframe
        )

    return TeamDepthChart(**depth_chart_data)


class Summary(FilterWidgets):
    """
    Scrapes the `Summary`_ tab of the FanGraphs **Teams** pages.

    _Note: The default team is the Los Angeles Angels of Anaheim

    .. _Summary: https://fangraphs.com/teams/angels/
    """
    _widget_class = teams_.Summary
    address = "https://fangraphs.com/teams/angels"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self)

        self.standings = None
        self.depth_chart = ()
        self._stat_tables = ()
        self.batting = None
        self.pitching = None

    def _get_data_table(self, table: bs4.Tag) -> pd.DataFrame:
        """

        :return:
        """
        def player_id_positions(row_elems: bs4.ResultSet) -> Generator[
            tuple[str, str], None, None
        ]:
            for row in row_elems:
                try:
                    elem = row.select("td")[0].select_one("a")
                    yield PID_POS_REGEX.search(
                        elem.attrs.get("href")
                    ).groups()
                except AttributeError:
                    yield "", ""

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe = dataframe.join(
            pd.DataFrame(
                player_id_positions(table_data.row_elems),
                columns=["PlayerID", "Positions"]
            )
        )
        dataframe.replace("", np.NaN, inplace=True)

        return dataframe

    @property
    def standings(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._standings

    @standings.setter
    def standings(self, value) -> None:
        """

        """
        table = self.soup.select_one("table.team-standings")

        def revise_columns(df: pd.DataFrame) -> pd.DataFrame:
            columns = list(df.columns)
            columns[0] = "Team"
            df.rename(columns=dict(zip(df.columns, columns)), inplace=True)
            return df

        table_data = self.scrape_table(
            table,
            css_h="tbody > tr:first-child", css_r="tbody > tr.team-row"
        )

        dataframe = revise_columns(table_data.dataframe)

        self._standings = dataframe

    @property
    def depth_chart(self) -> TeamDepthChart:
        """

        :return:
        """
        return self._depth_chart

    @depth_chart.setter
    def depth_chart(self, value) -> None:
        """

        """
        self._depth_chart = scrape_depth_chart(self.soup)

    @property
    def _stat_tables(self) -> dict[str, bs4.Tag]:
        """

        :return:
        """
        return self.__stat_tables

    @_stat_tables.setter
    def _stat_tables(self, value) -> None:
        """

        """
        table_elems = self.soup.select(".team-stats-table")
        table_names = [
            e.text.title() for e in self.soup.select("h2.team-header")
        ]

        self.__stat_tables = dict(zip(table_names, table_elems))

    @property
    def batting(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._batting

    @batting.setter
    def batting(self, value) -> None:
        """

        """
        self._batting = self._get_data_table(
            self._stat_tables["Batting Stats Leaders"]
        )

    @property
    def pitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._pitching

    @pitching.setter
    def pitching(self, value) -> None:
        """

        """
        self._pitching = self._get_data_table(
            self._stat_tables["Pitching Stats Leaders"]
        )


class Stats(FilterWidgets):
    """
    Scrapes the `Stats`_ tab of the FanGraphs **Teams** pages.

    .. _Stats: https://fangraphs.com/teams/angels/stats
    """
    _widget_class = teams_.Stats
    address = "https://fangraphs.com/teams/angels/stats"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.depth_chart = ()

        self._stat_tables = ()
        self.batting = None
        self.spitching = None
        self.rpitching = None
        self.fielding = None

    def _get_data_table(self, table: bs4.Tag) -> pd.DataFrame:
        """

        :return:
        """
        def player_id_positions(row_elems: bs4.ResultSet) -> Generator[
            tuple[str, str], None, None
        ]:
            for row in row_elems:
                try:
                    elem = row.select("td")[0].select_one("a")
                    yield PID_POS_REGEX.search(
                        elem.attrs.get("href")
                    ).groups()
                except AttributeError:
                    yield "", ""

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe = dataframe.join(
            pd.DataFrame(
                player_id_positions(table_data.row_elems),
                columns=["PlayerID", "Positions"]
            )
        )
        dataframe.replace("", np.NaN, inplace=True)

        return dataframe

    @property
    def _stat_tables(self) -> dict[str, bs4.Tag]:
        """

        :return:
        """
        return self.__stat_tables

    @_stat_tables.setter
    def _stat_tables(self, value) -> None:
        """

        """
        table_elems = self.soup.select(".team-stats-table")
        table_names = [
            e.text.title() for e in self.soup.select("h2.team-header")
        ]

        self.__stat_tables = dict(zip(table_names, table_elems))

    @property
    def batting(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._batting

    @batting.setter
    def batting(self, value) -> None:
        """

        """
        self._batting = self._get_data_table(
            self._stat_tables["Batting Stats Leaders"]
        )

    @property
    def spitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._spitching

    @spitching.setter
    def spitching(self, value) -> None:
        """

        """
        self._spitching = self._get_data_table(
            self._stat_tables["Starting Pitching Stats Leaders"]
        )

    @property
    def rpitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._rpitching

    @rpitching.setter
    def rpitching(self, value) -> None:
        """

        """
        self._rpitching = self._get_data_table(
            self._stat_tables["Relief Pitching Stats Leaders"]
        )

    @property
    def fielding(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._fielding

    @fielding.setter
    def fielding(self, value) -> None:
        """

        """
        self._fielding = self._get_data_table(
            self._stat_tables["Fielding Stats Leaders"]
        )


class Schedule(FilterWidgets):
    """
    Scrapes the `Schedule`_ tab of the FanGraphs **Teams** pages.

    .. _Schedule: https://fangraphs.com/tames/angels/schedule
    """
    _widget_class = teams_.Schedule
    address = "https://fangraphs.com/teams/angels/schedule"

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

        """
        table = self.soup.select_one("div.team-schedule-table > table")

        def revise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
            index = [
                df.columns[3], df.columns[5], df.columns[6]
            ]
            df[index] = df[index].replace("", np.NaN)
            return df

        def revise_columns(df: pd.DataFrame) -> pd.DataFrame:
            columns = list(df.columns)
            columns[1] = "vs/at"
            df.rename(columns=dict(zip(df.columns, columns)), inplace=True)
            return df

        def revise_dates(row_elems: bs4.ResultSet) -> Generator[
            datetime.datetime, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[0].select_one("span.date-full")
                date = datetime.datetime.strptime(
                    elem.text, "%b %d, %Y"
                )
                yield date

        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            tuple[str, str], None, None
        ]:
            for row in row_elems:
                elems = (e.select_one("a") for e in row.select("td")[-2:])
                yield tuple(
                    PID_REGEX.search(e.attrs.get("href")).group(1)
                    for e in elems
                )

        table_data = self.scrape_table(
            table, css_h="tr:first-child", css_r="tr:not(tr:first-child)"
        )

        dataframe = revise_dataframe(revise_columns(table_data.dataframe))
        dataframe["Date"] = tuple(revise_dates(table_data.row_elems))
        dataframe = dataframe.join(
            pd.DataFrame(
                get_player_id(table_data.row_elems),
                columns=[f"{p} PlayerID" for p in dataframe.columns[-2:]]
            )
        )

        self._data = dataframe


class PlayerUsage(FilterWidgets):
    """
    Scrapes the `Player Usage`_ tab of the FanGraphs **Teams** pages.

    .. _Player Usage: https://fangraphs.com/teams/angels/player-usage
    """
    _widget_class = teams_.PlayerUsage
    address = "https://fangraphs.com/teams/angels/player-usage"

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

        """
        table = self.soup.select_one(".table-scroll")

        def revise_columns(df: pd.DataFrame) -> pd.DataFrame:
            columns = list(df.columns)
            columns[2:11] = list(range(1, 10))
            df.rename(columns=dict(zip(df.columns, columns)), inplace=True)
            return df

        def revise_dates(row_elems: bs4.ResultSet) -> Generator[
            datetime.datetime, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[0].select_one("a")
                date = datetime.datetime.strptime(
                    elem.text, "%m/%d/%Y"
                )
                yield date

        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[1].select_one("a")
                yield PID_REGEX.search(elem.attrs.get("href")).group(1)

        table_data = self.scrape_table(table)

        dataframe = revise_columns(table_data.dataframe)
        dataframe["Game Date"] = tuple(revise_dates(table_data.row_elems))
        dataframe["Opp SP PlayerID"] = tuple(get_player_id(table_data.row_elems))

        self._data = dataframe


class DepthChart(FilterWidgets):
    """
    Scrapes the `Depth Chart`_ tab of the FanGraphs **Teams** page.

    .. _Depth Chart: https://fangraphs.com/teams/angels/depth-chart
    """
    _widget_class = teams_.DepthChart
    address = "https://fangraphs.com/teams/angels/depth-chart"

    class DepthChartTables(NamedTuple):
        p_C: pd.DataFrame
        p_1B: pd.DataFrame
        p_2B: pd.DataFrame
        p_3B: pd.DataFrame
        p_SS: pd.DataFrame
        p_LF: pd.DataFrame
        p_CF: pd.DataFrame
        p_RF: pd.DataFrame
        p_DH: pd.DataFrame

        p_RP: pd.DataFrame
        p_SP: pd.DataFrame

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.depth_chart = None

        self._dchart_tables = ()
        self.depth_chart_tables = ()
        self.batting = None
        self.pitching = None

    def _get_data_table(self, table: bs4.Tag) -> pd.DataFrame:
        """

        :param table:
        :return:
        """
        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select_one("td.frozen > a")
                yield PID_REGEX.search(elem.attr.get("href").group(1))

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe["PlayerID"] = tuple(get_player_id(table_data.row_elems))

        return dataframe

    def _get_dchart_table(self, table: bs4.Tag) -> pd.DataFrame:
        """

        :param table:
        :return:
        """
        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                try:
                    elem = row.select_one("td.frozen > a")
                    yield PID_REGEX.search(elem.attrs.get("href")).group(1)
                except AttributeError:
                    yield ""

        def get_injury(row_elems: bs4.ResultSet) -> Generator[
            Optional[str], None, None
        ]:
            for row in row_elems:
                elem = row.select_one("td.frozen > a > img.depth-table-injury")
                try:
                    yield elem.attrs.get("tooltip")
                except AttributeError:
                    yield None

        table_data = self.scrape_table(
            table,
            css_h="tbody > tr:first-child",
            css_r="tbody > tr:not(tr:first-child)"
        )

        dataframe = table_data.dataframe
        dataframe["PlayerID"] = tuple(get_player_id(table_data.row_elems))
        dataframe["Injury"] = tuple(get_injury(table_data.row_elems))

        return dataframe

    @property
    def depth_chart(self) -> TeamDepthChart:
        """

        :return:
        """
        return self._depth_chart

    @depth_chart.setter
    def depth_chart(self, value) -> None:
        """

        """
        self._depth_chart = scrape_depth_chart(self.soup)

    @property
    def _dchart_tables(self) -> dict[str, bs4.Tag]:
        """

        :return:
        """
        return self.__dchart_tables

    @_dchart_tables.setter
    def _dchart_tables(self, value) -> None:
        """

        """
        batting = self.soup.select(".team-depth-table-bat")
        batting_tnames = [
            e.select_one("div.team-depth-table-pos.team-color-primary").text
            for e in batting
        ][:-1]
        batting_tnames = (f"p_{pos}" for pos in batting_tnames)
        batting_tables = [
            e.select_one(
                "div.team-stats-table > div.outer > div.inner > table"
            ) for e in batting
        ]
        batting_dchart_tables = dict(zip(batting_tnames, batting_tables))

        pitching = self.soup.select(".team-depth-table-pit")
        pitching_tnames = [
            e.select_one("div.team-depth-table-pos.team-color-primary").text
            for e in pitching
        ][:-1]
        pitching_tnames = (f"p_{pos}" for pos in pitching_tnames)
        pitching_tables = [
            e.select_one(
                "div.team-stats-table > div.outer > div.inner > table"
            ) for e in pitching
        ]
        pitching_dchart_tables = dict(zip(pitching_tnames, pitching_tables))

        depth_chart_tables = {
            "Batting": batting_tables[-1], "Pitching": pitching_tables[-1]
        }
        depth_chart_tables.update(batting_dchart_tables)
        depth_chart_tables.update(pitching_dchart_tables)

        self.__dchart_tables = depth_chart_tables

    @property
    def depth_chart_tables(self) -> tuple:
        """

        :return:
        """
        return self._depth_chart_tables

    @depth_chart_tables.setter
    def depth_chart_tables(self, value) -> None:
        """

        """
        dchart_tables = self._dchart_tables.copy()
        del dchart_tables["Batting"], dchart_tables["Pitching"]

        data = {}
        for tname, table in dchart_tables.items():
            data[tname] = self._get_dchart_table(table)

        self._depth_chart_tables = self.DepthChartTables(**data)

    @property
    def batting(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._batting

    @batting.setter
    def batting(self, value) -> None:
        """

        """
        table = self._dchart_tables["Batting"]
        table_data = self.scrape_table(
            table,
            css_h="tbody > tr:first-child",
            css_r="tbody > tr:not(tr:first-child)"
        )
        self._batting = table_data.dataframe

    @property
    def pitching(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._pitching

    @pitching.setter
    def pitching(self, value) -> None:
        """

        """
        table = self._dchart_tables["Pitching"]
        table_data = self.scrape_table(
            table,
            css_h="tbody > tr:first-child",
            css_r="tbody > tr:not(tr:first-child)"
        )
        self._pitching = table_data.dataframe
