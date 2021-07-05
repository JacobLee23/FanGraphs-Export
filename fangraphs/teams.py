#! usr/bin/env python
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.

Note: The default team is the Los Angeles Angels of Anaheim.
Thus, the base URL always navigates to the stats concerning the Angels.
"""

import datetime
import re
from typing import *

import bs4
import numpy as np
import pandas as pd

from fangraphs import PID_REGEX, PID_POS_REGEX
from fangraphs import FilterWidgets
from fangraphs.selectors import teams_


def _get_table_headers(table, header_elem: str):
    """
    Scrapes the table headers off of the stat leaders data_tables table.

    :param table: The data_tables table element
    :type table: playwright.sync_api._generated.ElementHandle
    :param header_elem: A table headers CSS selector
    :return: An empty DataFrame with columns set to the table headers
    :rtype: pd.DataFrame
    """
    headers = [
        e.text_content() for e in table.query_selector_all(
            header_elem
        )
    ]
    headers.extend(["Player ID", "Position(s)"])
    dataframe = pd.DataFrame(columns=headers)

    return dataframe


def _scrape_data_table(table, header_elem="thead > tr > th"):
    """
    Scrapes the data_tables table.

    :param table: The data_tables table element
    :type table: playwright.sync_api._generated.ElementHandle
    :param header_elem: A table headers CSS selector
    :return: A DataFrame of the table data_tables.
    :rtype: pd.DataFrame
    """
    dataframe = _get_table_headers(table, header_elem)

    rows = table.query_selector_all("tbody > tr[role='row']")
    href_regex = re.compile(r"/statss\.aspx\?playerid=(\d+)&position=(.*)")

    for i, row in enumerate(rows):
        data = [e.text_content() for e in row.query_selector_all("td")]

        # Get player ID and position(s)
        href = row.query_selector("td.frozen > a").get_attribute("href")
        player_id, position = href_regex.search(href).groups()
        data.extend([int(player_id), position])

        # Update DataFrame
        dataframe.loc[i] = data

    # Get table totals
    foot = table.query_selector("tfoot > tr[role='row']")
    footer_row = [e.text_content() for e in foot.query_selector_all("td")]
    footer_row.extend([np.NaN, ""])

    # Update DataFrame
    dataframe.loc["Total"] = footer_row

    return dataframe


def _scrape_positional_data(page, pos_num: int):
    """
    Scrapes the depth chart data_tables for the specified position.

    :param page: A Playwright ``Page`` object
    :type page: playwright.sync_api._generated.Page
    :param pos_num: The positional number
    :return: The position name and the zipped player names and stats
    :rtype: tuple[
        str, list[tuple[playwright.sync_api._generated.ElementHandle]]
    ]
    """
    position = page.query_selector(f"#pos{pos_num}")

    position_name = position.query_selector(
        f"text#pos-label{pos_num}"
    ).text_content()
    player_stats = zip(
        position.query_selector_all("text.player-name"),
        position.query_selector_all("text.player-stat")
    )
    return position_name, player_stats


def _scrape_depth_chart(page, pos_nums):
    """
    Scrapes the positional depth chart data_tables off of the depth chart diagrams.

    **Position numbers**:

    +---------------+---------------+---------------+---------------+
    | ``0``: RP     | ``1``: SP     | ``2``: C      | ``3``: 1B     |
    +---------------+---------------+---------------+---------------+
    | ``4``: 2B     | ``5``: 3B     | ``6``: SS     | ``7``: LF     |
    +---------------+---------------+---------------+---------------+
    | ``8``: CF     | ``9``: RF     | ``10``: DH    |               |
    +---------------+---------------+---------------+---------------+

    :param page: A Playwright ``Page`` object
    :type page: playwright.sync_api._generated.Page
    :param pos_nums: A sequence of positional numbers to scrape
    :return: A dictionary of positions to a DataFrame of positional depth chart data_tables
    :rtype: dict[str, pd.DataFrame]
    """
    data = {}
    href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

    for i in pos_nums:
        # Initialize DataFrame
        dataframe = pd.DataFrame(columns=("Name", "Stat", "Player ID"))

        # Get position name and corresponding players
        position_name, player_stats = _scrape_positional_data(page, i)

        for j, (player, stat) in enumerate(player_stats):
            player_name, stat_value = player.text_content(), stat.text_content()

            # Get player ID
            if not (player_name and stat_value):
                continue
            try:
                href = player.query_selector("a").get_attribute("href")
                player_id = href_regex.search(href).group(1)
            except AttributeError:
                player_id = np.NaN

            # Update DataFrame
            dataframe.loc[j] = (player_name, stat_value, player_id)

        # Update dictionary with position and DataFrame
        data.setdefault(position_name, dataframe)

    return data


def scrape_depth_chart(soup: bs4.BeautifulSoup) -> pd.Series[pd.DataFrame]:
    """

    :param soup:
    :return:
    """
    depth_chart_data = {}

    def get_player_id(elem: bs4.Tag) -> Optional[str]:
        match = PID_REGEX.search(
            elem.select_one("a").attrs.get("href")
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
        player_elems = zip(player_name_elems, player_stat_elems)

        players = [
            (e1.text, e2.text, get_player_id(e1))
            for (e1, e2) in player_elems
            if (e1.text and e2.text)
        ]

        dataframe = pd.DataFrame(
            data=players, columns=["Name", "Stat", "PlayerID"]
        )
        depth_chart_data.setdefault(
            f"p_{position}", dataframe
        )

    return pd.Series(
        depth_chart_data
    )


class Summary(FilterWidgets):
    """
    Scrapes the `Summary`_ tab of the FanGraphs **Teams** pages.

    _Note: The default team is the Los Angeles Angels of Anaheim

    .. _Summary: https://fangraphs.com/teams/angels/
    """
    _widget_class = teams_.Summary
    address = "https://fangraphs.com/teams/angels"

    class DataTables(NamedTuple):
        batting_stats_leaders: pd.DataFrame
        pitching_stats_leaders: pd.DataFrame
        depth_chart: pd.Series[pd.DataFrame]

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self)

        self.data_tables = ()

    @property
    def data_tables(self) -> DataTables:
        """

        :return:
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, value) -> None:
        """

        """
        table_elems = self.soup.select(".team-stats-table")
        table_names = [
            "".join(e.text.lower().split())
            for e in self.soup.select("h2.team-header")
        ]

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

        data = {}
        for table, tname in zip(table_elems, table_names):
            table_data = self.scrape_table(table)

            dataframe = table_data.dataframe
            dataframe["PlayerID"], dataframe["Positions"] = player_id_positions(
                table_data.row_elems
            )
            data[tname] = dataframe

        data["depth_chart"] = scrape_depth_chart(self.soup)

        self._data_tables = self.DataTables(**data)


class Stats(FilterWidgets):
    """
    Scrapes the `Stats`_ tab of the FanGraphs **Teams** pages.

    .. _Stats: https://fangraphs.com/teams/angels/stats
    """
    _widget_class = teams_.Stats
    address = "https://fangraphs.com/teams/angels/stats"

    class DataTables(NamedTuple):
        batting_stat_leaders: pd.DataFrame
        starting_pitching_stat_leaders: pd.DataFrame
        relief_pitching_stat_leaders: pd.DataFrame
        fielding_stat_leaders: pd.DataFrame

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data_tables = None

    @property
    def data_tables(self) -> DataTables:
        """

        :return:
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, value) -> None:
        """

        """
        table_elems = self.soup.select(".team-stats-table")
        table_names = [
            "".join(e.text.lower().split())
            for e in self.soup.select("h2.team-header")
        ]

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

        data = {}
        for table, tname in zip(table_elems, table_names):
            table_data = self.scrape_table(table)

            dataframe = table_data.dataframe
            dataframe["PlayerID"], dataframe["Positions"] = player_id_positions(
                table_data.row_elems
            )
            data[tname] = dataframe

        self._data_tables = self.DataTables(**data)


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
        table_elem = self.soup.select_one("div.team-schedule-table > table")

        def revise_columns(df: pd.DataFrame) -> pd.DataFrame:
            columns = df.columns
            columns[1] = "vs/at"
            df.rename(columns=dict(zip(df.columns, columns)), inplace=True)
            return df

        def revise_dates(row_elems: bs4.ResultSet) -> Generator[
            datetime.datetime, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[0].select_one("a > span.date-full")
                date = datetime.datetime.strptime(
                    elem.text, "%b %m, %Y"
                )
                yield date

        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            tuple[str, str], None, None
        ]:
            for row in row_elems:
                elems = (
                    row.select("td")[-2].select_one("a"),
                    row.select("td")[-1].select_one("a")
                )
                yield (
                    PID_REGEX.search(elems[0].attrs.get("href").group(1)),
                    PID_REGEX.serach(elems[1].attrs.get("href").group(1))
                )

        table_data = self.scrape_table(
            table_elem, css_h="tr:first-child", css_r="tr:not(tr:first-child)"
        )
        dataframe = table_data.dataframe

        dataframe = revise_columns(dataframe)
        dataframe["Date"] = revise_dates(table_data.row_elems)
        pitchers = dataframe.columns[-2:]
        (dataframe[f"{pitchers[0]} PlayerID"],
         dataframe[f"{pitchers[1]} PlayerID"]) = get_player_id(
            table_data.row_elems
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
                elem = row.select("td")[0].select_one("a")
                yield PID_REGEX.search(elem.attr.get("href").group(1))

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe["Game Date"] = revise_dates(table_data.row_elems)
        dataframe["Opp SP PlayerID"] = get_player_id(table_data.row_elems)

        self._data = dataframe


class DepthChart(FilterWidgets):
    """
    Scrapes the `Depth Chart`_ tab of the FanGraphs **Teams** page.

    .. _Depth Chart: https://fangraphs.com/teams/angels/depth-chart
    """
    _widget_class = teams_.DepthChart
    address = "https://fangraphs.com/teams/angels/depth-chart"

    class DataTables(NamedTuple):
        p_C: pd.DataFrame
        p_1B: pd.DataFrame
        p_2B: pd.DataFrame
        p_3B: pd.DataFrame
        p_SS: pd.DataFrame
        p_LF: pd.DataFrame
        p_CF: pd.DataFrame
        p_RF: pd.DataFrame
        p_DH: pd.DataFrame
        batting: pd.DataFrame

        p_SP: pd.DataFrame
        p_RP: pd.DataFrame
        pitching: pd.DataFrame

        depth_chart: pd.Series[pd.DataFrame]

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data_tables = None

    @property
    def data_tables(self):
        """

        :return:
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, value) -> None:
        """

        """
        batting_tables = self.soup.select(".team-depth-table-bat")
        pitching_tables = self.soup.select(".team-depth-table-pit")

        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select_one("td.frozen > a")
                yield PID_REGEX.search(elem.attr.get("href").group(1))

        data = {}
        for table in (batting_tables+pitching_tables):
            table_data = self.scrape_table(table)

            tname = table.select_one(
                ".team-depth-table-pos.team-color-primary"
            ).text
            if tname == "ALL":
                tname = "batting" if table in batting_tables else "pitching"
            else:
                tname = f"p_{tname}"

            dataframe = table_data.dataframe
            dataframe["PlayerID"] = get_player_id(table_data.row_elems)

            data[tname] = dataframe

        data["depth_chart"] = scrape_depth_chart(self.soup)

        self._data_tables = self.DataTables(**data)
