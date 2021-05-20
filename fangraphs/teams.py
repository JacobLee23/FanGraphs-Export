#! python3
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.
"""

import re

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import teams_sel


class Summary(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Teams`_ pages.

    .. _Teams: https://fangraphs.com/teams
    """

    address = "https://fangraphs.com/teams"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.Summary)

    @staticmethod
    def _write_table_headers(node):
        """

        :return:
        :rtype: pd.DataFrame
        """
        elems = node.query_selector_all("thead > tr > th")
        headers = [e.text_content() for e in elems]
        headers.extend(["Player ID", "Position(s)"])
        dataframe = pd.DataFrame(columns=headers)
        return dataframe

    @staticmethod
    def _write_table_rows(dataframe, node):
        """

        :param dataframe:
        :type dataframe: pd.DataFrame
        :param node:
        :type node: playwright.sync_api._generated.ElementHandle
        :return:
        :rtype: pd.DataFrame
        """
        elems = node.query_selector_all("tr[role='row']")
        regex = re.compile(r"/statss\.aspx\?playerid=(\d+)&position=(.*)")
        for i, elem in enumerate(elems):
            row = [e.text_content() for e in elem.query_selector_all("td")]
            href = elem.query_selector("a[href]").get_attribute("href")
            pid, pos = regex.search(href).groups()
            row.extend([int(pid), pos])
            dataframe.loc[i] = row
        return dataframe

    def export(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        self._close_ad()
        data = {}

        groups = self.page.query_selector_all(".team-stats-table")
        stats = ("Batting Stat Leaders", "Pitching Stat Leaders")
        for group, stat in zip(groups, stats):
            data.setdefault(stat)
            dataframe = self._write_table_headers(group)
            dataframe = self._write_table_rows(dataframe, group)
            data[stat] = dataframe

        data.setdefault("Depth Chart")
