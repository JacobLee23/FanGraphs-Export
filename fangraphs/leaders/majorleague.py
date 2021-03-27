#! python3
# FanGraphs/leaders/majorleague.py

"""
Scraper for the Major League Leaders page.
"""
import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs.selectors import leaders_sel


class MajorLeague(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Major League Leaderboards`_ page.

    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`.

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """
    __selections = leaders_sel.MajorLeague.selections
    __dropdowns = leaders_sel.MajorLeague.dropdowns
    __dropdown_options = leaders_sel.MajorLeague.dropdown_options
    __checkboxes = leaders_sel.MajorLeague.checkboxes
    __buttons = leaders_sel.MajorLeague.buttons

    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset()

    @classmethod
    def list_queries(cls):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        queries = []
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        queries.extend(list(cls.__checkboxes))
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
        if query in self.__checkboxes:
            options = ["True", "False"]
        elif query in self.__dropdown_options:
            elems = self.soup.select(f"{self.__dropdown_options[query]} li")
            options = [e.getText() for e in elems]
        elif query in self.__selections:
            elems = self.soup.select(f"{self.__selections[query]} li")
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
        if query in self.__checkboxes:
            elem = self.soup.select(self.__checkboxes[query])[0]
            option = "True" if elem.get("checked") == "checked" else "False"
        elif query in self.__dropdowns:
            elem = self.soup.select(self.__dropdowns[query])[0]
            option = elem.get("value")
        elif query in self.__selections:
            elem = self.soup.select(f"{self.__selections[query]} .rtsLink.rtsSelected")
            option = elem.getText()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=True):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, any buttons attached to the filter query will be clicked
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query, option = query.lower(), str(option).lower()
        if query not in self.list_queries():
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        if query in self.__buttons and autoupdate:
            self.__click_button(query)
        self._refresh_parser()

    def __configure_selection(self, query, option):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.click("#LeaderBoard_tsType a[href='#']")
        elem = self.page.query_selector_all(
            f"{self.__selections[query]} li"
        )[index]
        elem.click()

    def __configure_dropdown(self, query, option):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(
            self.__dropdowns[query]
        )
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > ul > li"
        )[index]
        elem.click()

    def __configure_checkbox(self, query, option):
        """
        Configures a checkbox-class filter query to an option.

        :param query: The checkbox-class filter query to be configured
        :param option: The option to set the filter query to
        """
        options = self.list_options(query)
        if option not in options:
            raise fangraphs.exceptions.InvalidFilterOption(query, option)
        if option != self.current_option(query).title():
            self.page.click(self.__checkboxes[query])

    def __click_button(self, query):
        """
        Clicks the button element which is attached to the search query.

        :param query: The filter query which has an attached form submission button
        """
        self.page.click(
            self.__buttons[query]
        )

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#LeaderBoard1_cmdCSV", path)
