#! python3
# fangraphs/teams/__init__.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.
"""

import csv
import os

from fangraphs import ScrapingUtilities
from fangraphs import selectors
import fangraphs.exceptions
from fangraphs.selectors import teams_sel


class DepthCharts(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Depth Charts`_ page.

    .. _Depth Charts: https://fangraphs.com/depthcharts.aspx
    """
    __selections = {}
    __dropdowns = {}

    address = "https://fangraphs.com/depthcharts.aspx"

    def __init__(self):
        super().__init__(
            self.address, selector_mod=teams_sel.DepthCharts
        )
        self.__enter__()

    def __enter__(self):
        self._browser_init()
        self.reset()
        self.__compile_selectors()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.quit()

    def __compile_selectors(self):
        for cat, sel in teams_sel.DepthCharts.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> div > ul > li")
            )
        for cat, sel in teams_sel.DepthCharts.dropdowns.items():
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> ul > a")
            )

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            options = self.__selections[query].list_options()
        elif query in self.__dropdowns:
            options = self.__dropdowns[query].list_options()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__selections[query].configure(self.page, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)

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
            current_type, self.soup, path
        )
        exp.export()


class Team(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Teams`_ page.

    .. _Team: https://fangraphs.com/teams
    """
    __selections = {}
    __dropdowns = {}

    address = "https://fangraphs.com/teams"

    def __init__(self):
        super().__init__(
            self.address, selector_mod=teams_sel.Teams
        )
        self.__enter__()

    def __enter__(self):
        self._browser_init()
        self.reset()
        self.__compile_selectors()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.quit()

    def __compile_selectors(self):
        for cat, sel in teams_sel.Teams.selections:
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> .cell")
            )
        for cat, sel in teams_sel.Teams.dropdowns:
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> option")
            )

    @classmethod
    def list_queries(cls):
        pass

    def list_options(self, query: str):
        pass

    def current_option(self, query: str):
        pass

    def configure(self, query: str, option: str):
        pass

    def export(self, *, path):
        pass


class _Export:
    """
    Exports the **Depth Charts** data tables.
    """
    headers = "thead > tr > th"
    rows = "tr[class*='depth']"
    tables = "#content > div > table"
    table_names = "#content > div > a"

    def __init__(self, ttype, soup, path):
        self.ttype = ttype.lower()
        self.soup = soup
        if not os.path.isdir(path):
            raise Exception(
                "Argument 'path' must be a valid path to a directory"
            )
        self.path = os.path.normpath(path)

    def _get_tables(self):
        """
        Returns all the data tables on the current page

        :return: A dictionary of the data table names to the table element
        :rtype: dict[str, bs4.BeautifulSoup]
        """
        tables_sel = self.soup.select(self.tables)
        tnames_sel = self.soup.select(self.table_names)
        tnames = [e.getText() for e in tnames_sel]
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
        """
        elems = node.select(headers_sel)
        headers = [e.getText() for e in elems]
        writer.writerow(headers)

    @staticmethod
    def _write_table_rows(writer: csv.writer, node, rows_sel):
        """
        Iterates through the rows of the current data table.
        The data in each row is written to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        elems = node.select(rows_sel)
        rows = [[e.getText() for e in row.select("td")] for row in elems]
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
