#! python3
# FanGraphs/leaders/international.py

"""
Scraper for the KBO Leaders page.
"""

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs.selectors import leaders_sel


class International(ScrapingUtilities):
    """
    Scrapes the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """
    __selections = leaders_sel.International.selections
    __dropdowns = leaders_sel.International.dropdowns
    __checkboxes = leaders_sel.International.checkboxes
    __waitfor = leaders_sel.International.waitfor

    address = "https://www.fangraphs.com/leaders/international"

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
        queries.extend(cls.__selections)
        queries.extend(cls.__dropdowns)
        queries.extend(cls.__checkboxes)
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
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} > div > a"
            )
            options = [e.getText() for e in elems]
        elif query in self.__checkboxes:
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
        option = ""
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "active" in elem.get("class"):
                    option = elem.getText()
                    break
        elif query in self.__dropdowns:
            elem = self.soup.select(
                f"{self.__dropdowns[query]} > div > span"
            )[0]
            option = elem.getText()
        elif query in self.__checkboxes:
            elem = self.soup.select(
                self.__selections["stat"][0]
            )
            option = "True" if ",to" in elem[0].get("href") else "False"
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
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption from err
        self.page.click(
            self.__selections[query][index]
        )

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
            raise fangraphs.exceptions.InvalidFilterOption from err
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > a"
        )[index]
        elem.click()

    def __configure_checkbox(self, query: str, option: str):
        """
        Configures a checkbox-class filter query to an option.

        :param query: The checkbox-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        if option not in options:
            raise fangraphs.exceptions.InvalidFilterOption
        if option == self.current_option(query):
            return
        self.page.click(self.__checkboxes[query])

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data(".data-export", path)
