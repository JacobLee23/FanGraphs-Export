#! python3
# FanGraphs/leaders/international.py

"""
Scraper for the KBO Leaders page.
"""

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import leaders_sel


class International(ScrapingUtilities):
    """
    Scrapes the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """
    __selections = {}
    __dropdowns = {}
    __switches = {}
    __waitfor = leaders_sel.International.waitfor

    address = "https://www.fangraphs.com/leaders/international"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)
        self.compile_selectors()

    def compile_selectors(self):
        for cat, sel in leaders_sel.International.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel)
            )
        for cat, sel in leaders_sel.International.dropdowns.items():
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> div > a")
            )
        for cat, sel in leaders_sel.International.switches.items():
            self.__switches.setdefault(
                cat, selectors.Switches(self.soup, sel)
            )

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(cls.__selections)
        queries.extend(cls.__dropdowns)
        queries.extend(cls.__switches)
        return queries

    def list_options(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            options = self.__selections[query].list_options()
        elif query in self.__dropdowns:
            options = self.__dropdowns[query].list_options()
        elif query in self.__switches:
            options = ["True", "False"]
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """

        :param query:
        :return:
        """
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option(opt_type=3)
        elif query in self.__switches:
            option = "True" if ",to" in self.page.url else "False"
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
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__dropdowns[query].configure(self.page, option)
        elif query in self.__switches:
            options = [o.lower() for o in self.list_options(query)]
            if option not in options:
                raise fangraphs.exceptions.InvalidFilterOption(option)
            if option == self.current_option(query):
                return
            self.page.click(self.__switches[query])
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
        self.export_data(".data-export", path)
