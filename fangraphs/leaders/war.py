#! python3
# FanGraphs/leaders/war.py

"""
Scraper for the Combined WAR Leaderboards page.
"""

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs.selectors import leaders_sel


class WAR(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Combined WAR Leaderboards`_ page.

    .. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
    """
    __dropdowns = leaders_sel.WAR.dropdowns
    __dropdown_options = leaders_sel.WAR.dropdown_options
    __waitfor = leaders_sel.WAR.waitfor

    address = "https://fangraphs.com/warleaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

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
            elems = self.soup.select(
                f"{self.__dropdown_options[query]} > ul > li"
            )
            options = [e.getText() for e in elems]
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
            elem = self.soup.select(self.__dropdowns[query])[0]
            option = elem.get("value")
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
            self.__configure_dropdown(query, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdown_options} > ul > li"
        )[index]
        elem.click()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#WARBoard1_cmdCSV", path)
