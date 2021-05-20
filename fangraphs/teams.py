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


def _scrape_table_headers(node):
    """

    :return:
    :rtype: pd.DataFrame
    """
    elems = node.query_selector_all("thead > tr > th")
    headers = [e.text_content() for e in elems]
    headers.extend(["Player ID", "Position(s)"])
    dataframe = pd.DataFrame(columns=headers)
    return dataframe


def _scrape_table_rows(dataframe, node):
    """

    :param dataframe:
    :type dataframe: pd.DataFrame
    :param node:
    :type node: playwright.sync_api._generated.ElementHandle
    :return:
    :rtype: pd.DataFrame
    """
    elems = node.query_selector_all("tbody > tr[role='row']")
    regex = re.compile(r"/statss\.aspx\?playerid=(\d+)&position=(.*)")
    for i, elem in enumerate(elems):
        row = [e.text_content() for e in elem.query_selector_all("td")]
        try:
            href = elem.query_selector("td.frozen > a").get_attribute("href")
            pid, pos = regex.search(href).groups()
            row.extend([int(pid), pos])
        except AttributeError:
            row.extend([np.NaN, ""])
        dataframe.loc[i] = row
    foot = node.query_selector("tfoot > tr[role='row']")
    footer_row = [e.text_content() for e in foot.query_selector_all("td")]
    footer_row.extend([np.NaN, ""])
    dataframe.loc["Total"] = footer_row
    return dataframe


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

    def _scrape_dchart(self, pos_nums):
        """

        :param pos_nums:
        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        data_dict = {}
        regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")
        for i in pos_nums:
            dataframe = pd.DataFrame(columns=("Name", "Stat", "Player ID"))
            position = self.page.query_selector(f"g#pos{i}")
            pos_name = position.query_selector(f"text#pos-label{i}").text_content()
            player_stats = zip(
                position.query_selector_all("text.player-name"),
                position.query_selector_all("text.player-stat")
            )
            for j, (player, stat) in enumerate(player_stats):
                name, value = player.text_content(), stat.text_content()
                try:
                    href = player.query_selector("a").get_attribute("href")
                    pid = regex.search(href).group(1)
                except AttributeError:
                    pid = np.NaN
                dataframe.loc[j] = (name, value, pid)
            data_dict.setdefault(pos_name, dataframe)
        return data_dict

    def _write_depth_charts(self):
        """

        :return:
        :rtype: tuple[dict[str, pd.DataFrame]]
        """
        position_players = self._scrape_dchart(range(2, 11))
        pitchers = self._scrape_dchart(range(0, 2))
        return position_players, pitchers

    def export(self):
        """

        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        data = {}

        groups = self.page.query_selector_all(".team-stats-table")
        stats = ("Batting Stat Leaders", "Pitching Stat Leaders")
        for group, stat in zip(groups, stats):
            data.setdefault(stat)
            dataframe = _scrape_table_headers(group)
            dataframe = _scrape_table_rows(dataframe, group)
            data[stat] = dataframe

        data.setdefault("Depth Chart")
        pplayer_dchart, pitcher_dchart = self._write_depth_charts()
        data.update(pplayer_dchart)
        data.update(pitcher_dchart)

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

        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        data = {}

        groups = self.page.query_selector_all(".team-stats-table")
        stats = [e.text_content() for e in self.page.query_selector_all(
            "h2.team-header"
        )]
        for group, stat in zip(groups, stats):
            data.setdefault(stat)
            dataframe = _scrape_table_headers(group)
            dataframe = _scrape_table_rows(dataframe, group)
            data[stat] = dataframe

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

    def _scrape_table(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        elems = self.page.query_selector_all(
            ".team-schedule-table tbody > tr"
        )

        # Get header data
        header_elem = elems.pop(0)
        headers = [e.text_content() for e in header_elem.query_selector_all("th")]
        headers[1] = "VS/AT"
        headers.extend(
            [f"{headers[-2]} Player ID", f"{headers[-1]} Player ID"]
        )

        # Initialize objects
        dataframe = pd.DataFrame(columns=headers)
        regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(elems):
            data = [e.text_content() for e in row.query_selector_all("td")]

            # Rewrite date
            dates = (
                row.query_selector("span.date-full").text_content(),
                row.query_selector("span.date-short").text_content()
            )
            data[0] = f"{dates[0]} ({dates[1]})"

            # Add pitcher player IDs
            hrefs = row.query_selector_all("td.alignL.hi > a")
            pitcher_ids = [
                regex.search(h.get_attribute("href")).group(1)
                for h in hrefs
            ]
            if pitcher_ids:
                data.extend(pitcher_ids)
            else:
                data.extend([np.NaN, np.NaN])

            # Update DataFrame
            dataframe.loc[i] = data

        return dataframe

    def export(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        dataframe = self._scrape_table()
        return dataframe
