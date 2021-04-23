#! python3
# fangraphs/teams/__init__.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.
"""

import csv
import os

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

    def export(self, *, path):
        """
        Iterates through all the data tables on the current webpages.
        Writes the data to a CSV file, named by the name of the data table.
        All CSV files are stored in the directory specified by :py:attr:`path`.

        *Note: This is a 'manual' export of the data.
        In other words, the data is scraped from the table.
        This is unlike other forms of export where a button is clicked.
        Thus, there will be no record of a download when the data is exported.*

        :param path: The directory path to save the exported files to
        """
        self._close_ad()
        current_type = self.current_option("type")
        exp = _Export(
            current_type, self.page, path
        )
        exp.export()


class _Export:
    """
    Exports the **Depth Charts** data tables.
    """
    headers = "thead > tr > th"
    rows = "tr[class*='depth']"
    tables = "#content > div > table"
    table_names = "#content > div > a"

    def __init__(self, ttype, page, path):
        """

        :param ttype:
        :param page:
        :type page: playwright.sync_api._generated.Page
        :param path:
        """
        self.ttype = ttype.lower()
        self.page = page
        if not os.path.isdir(path):
            raise Exception(
                "Argument 'path' must be a valid path to a directory"
            )
        self.path = os.path.normpath(path)

    def _get_tables(self):
        """
        Returns all the data tables on the current page

        :return: A dictionary of the data table names to the table element
        :rtype: dict[str, playwright.sync_api._generated.ElementHandle]
        """
        tables_sel = self.page.query_selector_all(self.tables)
        tnames_sel = self.page.query_selector_all(self.table_names)
        tnames = [e.text_content() for e in tnames_sel]
        if self.ttype in ["standings", "baseruns", "totals"]:
            tnames.insert(0, "General")
        elif self.ttype in [
            "depth charts",
            "C", "1B", "2B", "3B", "LF", "CF", "RF", "SP", "RP", "DH"
        ]:
            tnames.append("General")
        else:
            raise Exception
        tables = dict(zip(tnames, tables_sel))
        return tables

    @staticmethod
    def _write_table_headers(writer: csv.writer, node, headers_sel):
        """
        Writes the headers of the data table to the CSV file.

        :param writer: The ``csv.writer`` object
        :param node:
        :type node: playwright.sync_api._generated.ElementHandle
        :param headers_sel:
        :rtype: None
        """
        elems = node.query_selector_all(headers_sel)
        headers = [e.text_content() for e in elems]
        writer.writerow(headers)

    @staticmethod
    def _write_table_rows(writer: csv.writer, node, rows_sel):
        """
        Iterates through the rows of the current data table.
        The data in each row is written to the CSV file.

        :param writer: The ``csv.writer`` object
        :param node:
        :type node: playwright.sync_api._generated.ElementHandle
        :param rows_sel:
        :rtype: None
        """
        elems = node.query_selector_all(rows_sel)
        rows = [
            [e.text_content() for e in row.query_selector_all("td")]
            for row in elems
        ]
        writer.writerows(rows)

    def export(self):
        """
        Iterates through all the data tables on the current webpages.
        Writes the data to a CSV file, named by the name of the data table.
        All CSV files are stored in the directory specified by :py:attr:`path`.
        """
        tables = self._get_tables()
        for tname, telem in tables.items():
            filepath = os.path.join(self.path, f"{tname}.csv")
            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                self._write_table_headers(writer, telem, self.headers)
                self._write_table_rows(writer, telem, self.rows)
