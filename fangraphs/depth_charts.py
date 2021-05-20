#! python3
# fangraphs/depth_charts.py

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import dcharts_sel


class DepthCharts(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Depth Charts`_ page.

    .. _Depth Charts: https://fangraphs.com/depthcharts.aspx
    """

    address = "https://fangraphs.com/depthcharts.aspx"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, dcharts_sel.DepthCharts)

    def _get_tables(self):
        """
        Gets the names and elements for each of the leaderboard tables on the page.

        :return: A dictionary of table names with the corresponding table element
        :rtype: dict[str, playwright.sync_api._generated.ElementHandle]
        """
        tables_sel = self.page.query_selector_all("#content > div > table")
        tnames_sel = self.page.query_selector_all("#content > div > a")
        tnames = [e.text_content() for e in tnames_sel]

        table_type = self.current_option("view_type").lower()
        if table_type in (
                "standings", "baseruns", "totals"
        ):
            tnames.insert(0, "General")
        elif table_type in (
            "depth charts", "c", "1b", "2b", "3b", "lf", "cf", "rf", "sp", "dh"
        ):
            tnames.append("General")
        else:
            raise Exception
        tables = dict(zip(tnames, tables_sel))
        return tables

    @staticmethod
    def _write_table_headers(node):
        """
        Initializes a new DataFrame with columns corresponding to the table headers.

        :param node:
        :type node: playwright.sync_api._generated.ElementHandle
        :return: A DataFrame with columns set to the table headers
        :rtype: pd.DataFrame
        """
        elems = node.query_selector_all("thead > tr > th")
        headers = [e.text_content() for e in elems]
        dataframe = pd.DataFrame(columns=headers)
        return dataframe

    @staticmethod
    def _write_table_rows(dataframe, node):
        """
        Writes the data from each of the rows of each of the tables to the DataFrame.

        :param dataframe: The DataFrame to modify
        :type dataframe: pd.DataFrame
        :param node: The element corresponding to the table to scrape
        :type node: playwright.sync_api._generated.ElementHandle
        :return: The DataFrame updated with all the table leaderboard data
        :rtype: pd.DataFrame
        """
        elems = node.query_selector_all("tr[class*='depth']")
        for i, elem in enumerate(elems):
            row = [e.text_content() for e in elem.query_selector_all("td")]
            dataframe.loc[i] = row
        return dataframe

    def export(self):
        """
        Exports the data in each leaderboard on the page as a DataFrame.

        :return: A dictionary of the table names mapped to a DataFrame containing the table data
        :rtype: dict[str, pd.DataFrame]
        """
        self._close_ad()
        data = {}

        tables = self._get_tables()
        for tname, telem in tables.items():
            data.setdefault(tname)
            dataframe = self._write_table_headers(telem)
            dataframe = self._write_table_rows(dataframe, telem)
            data[tname] = dataframe

        return data
