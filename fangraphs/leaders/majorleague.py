#! python3
# FanGraphs/leaders/majorleague.py

"""
Scraper for the Major League Leaders page.
"""
import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import leaders_sel


class MajorLeague(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Major League Leaderboards`_ page.

    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`.

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """
    __selections = {}
    __dropdowns = {}
    __switches = {}
    __buttons = leaders_sel.MajorLeague.buttons

    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset()
        self.compile_selectors()

    def compile_selectors(self):
        for cat, sel in leaders_sel.MajorLeague.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> div > ul > li")
            )
        for cat, sel in leaders_sel.MajorLeague.dropdowns.items():
            options = leaders_sel.MajorLeague.dropdown_options[cat]
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> div > ul > li", options)
            )
        for cat, sel in leaders_sel.MajorLeague.switches.items():
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
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        queries.extend(list(cls.__switches))
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
        if query in self.__switches:
            options = ["True", "False"]
        elif query in self.__dropdowns:
            options = self.__dropdowns[query].list_options()
        elif query in self.__selections:
            options = self.__selections[query].list_options()
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
        if query in self.__switches:
            option = self.__switches[query].current_option(opt_type=1)
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option(opt_type=1)
        elif query in self.__selections:
            option = self.__selections[query].current_option()
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
        self._close_ad()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__dropdowns[query].configure(self.page, option)
        elif query in self.__switches:
            options = [o.lower() for o in self.list_options(query)]
            if option.lower() not in options:
                raise fangraphs.exceptions.InvalidFilterOption(option)
            if option != self.current_option(query).title():
                self.page.click(self.__switches[query])
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        if query in self.__buttons and autoupdate:
            self.page.click(self.__buttons[query])
        self._refresh_parser()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data("#LeaderBoard1_cmdCSV", path)
