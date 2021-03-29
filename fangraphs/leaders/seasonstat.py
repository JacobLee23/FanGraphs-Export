#! python3
# fangraphs.leaders.seasonstat.py

"""
Scraper for the Season Stat Grid page.
"""

import csv
import datetime
import os

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import leaders_sel


class SeasonStat(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Season Stat Grid`_ page.

    .. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
    """
    __selections = {}
    __dropdowns = {}
    __waitfor = leaders_sel.SeasonStat.waitfor

    address = "https://fangraphs.com/leaders/season-stat-grid"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)
        self.compile_selectors()

    def compile_selectors(self):
        for cat, sel in leaders_sel.SeasonStat.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel)
            )
        for cat, sel in leaders_sel.SeasonStat.dropdowns.items():
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> ul > li")
            )

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be sued to modify search results.

        :return: Filter queries which can be used to modify search results
        :type: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtyp: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
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
        Retrieves the option which a filter query is currently configured to.

        :param query: The filter query
        :return: The option which the filter query is currently configured to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option(opt_type=2)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__dropdowns[query].configure(self.page, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def _write_table_headers(self, writer: csv.writer):
        """
        Writes the headers of the data table to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        elems = self.soup.select(".table-scroll thead tr th")
        headers = [e.getText() for e in elems]
        writer.writerow(headers)

    def _write_table_rows(self, writer: csv.writer):
        """
        Iterates through the rows of the current data table.
        The data in each row is written to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        row_elems = self.soup.select(".table-scroll tbody tr")
        for row in row_elems:
            elems = row.select("td")
            items = [e.getText() for e in elems]
            writer.writerow(items)

    def export(self, path=""):
        """
        Scrapes and saves the data from the table of the current leaderboards.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *out/%d.%m.%y %H.%M.%S.csv*.

        *Note: This is a 'manual' export of the data.
        In other words, the data is scraped from the table.
        This is unlike other forms of export where a button is clicked.
        Thus, there will be no record of a download when the data is exported.*

        :param path: The path to save the exported file to
        """
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        total_pages = int(
            self.soup.select(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            )[0].getText()
        )
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            self._write_table_headers(writer)
            for _ in range(0, total_pages):
                self._write_table_rows(writer)
                self.page.click(
                    ".table-page-control:nth-last-child(1) > .next"
                )
                self._refresh_parser(waitfor=self.__waitfor)
