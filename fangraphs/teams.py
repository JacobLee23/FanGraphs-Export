#! python3
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.

_Note: The default team is the Los Angeles Angels of Anaheim.
Thus, the base URL always navigates to the stats concerning the Angels._
"""

import re

import numpy as np
import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import teams_sel


def _get_table_headers(table, header_elem: str):
    """
    Scrapes the table headers off of the stat leaders data table.

    :param table: The data table element
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
    Scrapes each row of data off of the stat leaders data table.

    :param table: The data table element
    :type table: playwright.sync_api._generated.ElementHandle
    :param header_elem: A table headers CSS selector
    :return: A modified DataFrame containing the data in the stat leaders table
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
    Scrapes the depth chart data for the specified position.

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
    Scrapes the positional depth chart data off of the depth chart diagrams.

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
    :return: A dictionary of positions and a DataFrame of positional depth chart data
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


class Summary(ScrapingUtilities):
    """
    Scrapes the `Summary`_ tab of the FanGraphs **Teams** pages.

    _Note: The default team is the Los Angeles Angels of Anaheim

    .. _Summary: https://fangraphs.com/teams/angels/
    """

    address = "https://fangraphs.com/teams/angels"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.Summary)

    def export(self):
        """
        Scrapes the data tables and depth chart diagram.

        :return: A dictionary of tables names and a DataFrame of the table data
        :rtype: dict[str, pd.DataFrame]
        """
        data = {}

        tables = self.page.query_selector_all(".team-stats-table")
        tnames = [
            e.text_content() for e in self.page.query_selector_all(
                "h2.team-header"
            )
        ]
        for table, tname in zip(tables, tnames):
            dataframe = _scrape_data_table(table)
            data.setdefault(tname, dataframe)

        data.update(_scrape_depth_chart(self.page, range(2, 11)))
        data.update(_scrape_depth_chart(self.page, range(0, 2)))

        return data


class Stats(ScrapingUtilities):
    """
    Scrapes the `Stats`_ tab of the FanGraphs **Teams** pages.

    .. _Stats: https://fangraphs.com/teams/angels/stats
    """

    address = "https://fangraphs.com/teams/angels/stats"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.Stats)

    def export(self):
        """
        Scrapes the data tables.

        :return: A dictionary of the table names and a DataFrame of the table data
        :rtype: dict[str, pd.DataFrame]
        """
        data = {}

        tables = self.page.query_selector_all(".team-stats-table")
        tnames = [
            e.text_content() for e in self.page.query_selector_all(
                "h2.team-header"
            )
        ]
        for table, tname in zip(tables, tnames):
            dataframe = _scrape_data_table(table)
            data.setdefault(tname, dataframe)

        return data


class Schedule(ScrapingUtilities):
    """
    Scrapes the `Schedule`_ tab of the FanGraphs **Teams** pages.

    .. _Schedule: https://fangraphs.com/tames/angels/schedule
    """

    address = "https://fangraphs.com/teams/angels/schedule"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.Schedule)

    @staticmethod
    def get_table_headers(header_elem):
        """
        Scrapes the table headers.

        :param header_elem: The table header element
        :type header_elem: playwright.sync_api._generated.ElementHandle
        :return: An empty DataFrame with the columns set to the table headers
        :rtype: pd.DataFrame
        """
        headers = [
            e.text_content() for e in header_elem.query_selector_all("th")
        ]
        headers[1] = "vs/at"
        headers.extend([
            f"{headers[-2]} Player ID",
            f"{headers[-1]} Player ID"
        ])

        dataframe = pd.DataFrame(columns=headers)

        return dataframe

    def _scrape_data_table(self):
        """
        Scrapes the data table

        :return: A DataFrame of the table data
        :rtype: pd.DataFrame
        """
        rows = self.page.query_selector_all(
            ".team-schedule-table tbody > tr"
        )
        header_elem = rows.pop(0)

        dataframe = self.get_table_headers(header_elem)

        href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            data = [e.text_content() for e in row.query_selector_all("td")]

            # Edit dates
            dates = (
                row.query_selector("span.date-full").text_content(),
                row.query_selector("span.date-short").text_content()
            )
            data[0] = f"{dates[0]} ({dates[1]})"

            # Edit pitchers
            pitchers = (
                row.query_selector("td.alignL:nth-last-child(2)"),
                row.query_selector("td.alignL:nth-last-child(1)")
            )
            for pitch_elem, pitch in zip(pitchers, data[-2:]):
                if pitch and "probable" in pitch_elem.get_attribute("class"):
                    data[data.index(pitch)] = f"{pitch}*"

            # Get pitcher player IDs
            pitcher_ids = []
            for elem in pitchers:
                try:
                    href = elem.query_selector("a").get_attribute("href")
                    pitcher_ids.append(href_regex.search(href).group(1))
                except AttributeError:
                    pitcher_ids.append(np.NaN)
            data.extend(pitcher_ids)

            # Update DataFrame
            dataframe.loc[i] = data

        return dataframe

    def export(self):
        """
        Scrapes the data table.

        _Note: An asterisk (*) next to a pitcher's name denotes a probably start._

        :return: A DataFrame of the table data
        :rtype: pd.DataFrame
        """
        dataframe = self._scrape_data_table()
        return dataframe


class PlayerUsage(ScrapingUtilities):
    """
    Scrapes the `Player Usage`_ tab of the FanGraphs **Teams** pages.

    .. _Player Usage: https://fangraphs.com/teams/angels/player-usage
    """

    address = "https://fangraphs.com/teams/angels/player-usage"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.PlayerUsage)

    def _get_table_headers(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        elems = self.page.query_selector_all(".table-scroll thead > tr > th")
        headers = [e.text_content() for e in elems]
        headers.insert(2, "Opp SP Player ID")
        dataframe = pd.DataFrame(columns=headers)
        return dataframe

    def _scrape_data_tables(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        dataframe = self._get_table_headers()

        rows = self.page.query_selector_all(".table-scroll tbody > tr")
        href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            data = [e.text_content() for e in row.query_selector_all("td")]

            # Get opposing pitcher player ID
            href = row.query_selector(
                "td[data-stat='Opp SP'] > a"
            ).get_attribute("href")
            player_id = href_regex.search(href).group(1)
            data.insert(2, player_id)

            # Update DataFrame
            dataframe.loc[i] = data

        return dataframe

    def export(self):
        """
        Scrapes the data table.

        :return: A DataFrame of the table data
        :rtype: pd.DataFrame
        """
        dataframe = self._scrape_data_tables()
        return dataframe


class DepthChart(ScrapingUtilities):
    """
    Scrapes the `Depth Chart`_ tab of the FanGraphs **Teams** page.

    .. _Depth Chart: https://fangraphs.com/teams/angels/depth-chart
    """

    address = "https://fangraphs.com/teams/angels/depth-chart"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.DepthChart)

    @staticmethod
    def _get_table_headers(header_elem):
        """
        Scrapes the table headers.

        :param header_elem: The element corresponding to the data table headers
        :type header_elem: playwright.sync_api._generated.ElementHandle
        :return: An empty DataFrame containing the headers of the data table
        :rtype: pd.DataFrame
        """
        headers = [e.text_content() for e in header_elem.query_selector_all("th")]
        headers.insert(1, "Player ID")

        dataframe = pd.DataFrame(columns=headers)

        return dataframe

    def _scrape_data_table(self, table):
        """
        Scrapes the data tables.

        :param table: The data table element
        :type table: playwright.sync_api._generated.table
        :return: A DataFrame containing all the data in the data table
        :rtype: pd.DataFrame
        """
        rows = table.query_selector_all(".team-stats-table tbody > tr")

        # Process table headers
        header_elem = rows.pop(0)

        dataframe = self._get_table_headers(header_elem)
        href_regex = re.compile(r"^/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            data = [e.text_content() for e in row.query_selector_all("td")]

            # Get player ID
            href = row.query_selector("td.frozen > a").get_attribute("href")
            player_id = href_regex.search(href).group(1)
            data.insert(1, player_id)

            # Update DataFrame
            dataframe.loc[i] = data

        return dataframe

    def export(self):
        """
        Scrapes the data tables and depth chart diagram.

        :return: A dictionary of table names and a DataFrame of the table data
        :rtype: dict[str, pd.DataFrame]
        """
        data = {}

        batting = self.page.query_selector_all(".team-depth-chart-bat")
        pitching = self.page.query_selector_all(".team-depth-chart-pit")
        all_positions = batting + pitching

        for table in all_positions:
            tname = table.query_selector(
                ".team-depth-table-pos.team-color-primary"
            ).text_content()
            if tname == "ALL":
                tname = "Batters: ALL" if table in batting else "Pitchers: ALL"
            dataframe = self._scrape_data_table(table)
            data.setdefault(tname, dataframe)

        data.update(_scrape_depth_chart(self.page, range(2, 11)))
        data.update(_scrape_depth_chart(self.page, range(0, 2)))

        return data
