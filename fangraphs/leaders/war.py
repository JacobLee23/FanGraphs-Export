#! python3
# FanGraphs/leaders/war.py

"""
Scraper for the Combined WAR Leaderboards page.
"""

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import leaders_sel


class WAR(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Combined WAR Leaderboards`_ page.

    .. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
    """
    __dropdowns = {}
    __waitfor = leaders_sel.WAR.waitfor

    address = "https://fangraphs.com/warleaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)
        self.compile_selectors()

    def compile_selectors(self):
        for cat, sel in leaders_sel.WAR.dropdowns.items():
            options = leaders_sel.WAR.dropdown_options[cat]
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> div > ul > li", options)
            )

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__dropdowns))
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
        if query in self.__dropdowns:
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
        if query in self.__dropdowns:
            option = self.__dropdowns[query].current_option(opt_type=1)
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
        self._close_ad()
        if query in self.__dropdowns:
            self.__dropdowns[query].configure(self.page, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#WARBoard1_cmdCSV", path)
