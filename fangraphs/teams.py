#! python3
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.
"""

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import teams_sel


class DepthCharts(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Depth Charts`_ page.

    .. _Depth Charts: https://fangraphs.com/depthcharts.aspx
    """

    address = "https://fangraphs.com/depthcharts.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, teams_sel.DepthCharts)
        self.queries = teams_sel.DepthCharts(self.page)

    def _get_tables(self):
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
        elems = node.query_selector_all("thead > tr > th")
        headers = [e.text_content() for e in elems]
        dataframe = pd.DataFrame(columns=headers)
        return dataframe

    @staticmethod
    def _write_table_rows(dataframe, node):
        elems = node.query_selector_all("tr[class*='depth']")
        for i, elem in enumerate(elems):
            row = [e.text_content() for e in elem.query_selector_all("td")]
            dataframe.loc[i] = row
        return dataframe

    def export(self, *, cleanup=True):
        """
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
