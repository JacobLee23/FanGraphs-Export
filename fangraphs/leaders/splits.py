#! python3
# fangraphs/leaders/splits.py

"""
Scraper for the Splits Leaderboards page.
"""

import fangraphs.exceptions
from fangraphs.leaders import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import leaders_sel


class Splits(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Splits Leaderboards`_ page.

    .. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
    """
    __selections = {}
    __dropdowns = {}
    __splits = {}
    __quick_splits = leaders_sel.Splits.quick_splits
    __switches = {}
    __waitfor = leaders_sel.Splits.waitfor

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)
        self.compile_selectors()

        self.configure_filter_group("Show All")
        self.configure("auto_pt", "False", autoupdate=True)

    def compile_selectors(self):
        for cat, sel in leaders_sel.Splits.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel)
            )
        for cat, sel in leaders_sel.Splits.dropdowns.items():
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> ul > li")
            )
        for cat, sel in leaders_sel.Splits.splits.items():
            self.__splits.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> ul > li")
            )
        for cat, sel in leaders_sel.Splits.switches.items():
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
        queries.extend(list(cls.__splits))
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
        if query in self.__selections:
            options = self.__selections[query].list_options()
        elif query in self.__dropdowns:
            options = self.__dropdowns[query].list_options()
        elif query in self.__splits:
            options = self.__splits[query].list_options()
        elif query in self.__switches:
            options = ["True", "False"]
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option(s) which a filter query is currently set to.

        Most dropdown- and split-class filter queries can be configured to multiple options.
        For those filter classes, a list is returned, while other filter classes return a string.

        - Selection-class: ``str``
        - Dropdown-class: ``list``
        - Split-class: ``list``
        - Switch-class: ``str``

        :param query: The filter query being retrieved of its current option
        :return: The option(s) which the filter query is currently set to
        :rtype: str or list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        elif query in self.__dropdowns:
            option = self.__dropdowns[query].current_option(opt_type=2, multiple=True)
        elif query in self.__splits:
            option = self.__splits[query].current_option(opt_type=2, multiple=True)
        elif query in self.__switches:
            option = self.__switches[query].current_option(opt_type=2)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=False):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, :py:meth:`update` will be called following configuration
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        self._close_ad()
        query = query.lower()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        elif query in self.__dropdowns:
            self.__dropdowns[query].configure(self.page, option)
        elif query in self.__splits:
            self.__splits[query].configure(self.page, option)
        elif query in self.__switches:
            options = [o.lower() for o in self.list_options(query)]
            if option.lower() not in options:
                raise fangraphs.exceptions.InvalidFilterOption(option)
            if option != self.current_option(query)[0].title():
                self.page.click(self.__switches[query])
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        if autoupdate:
            self.update()
        self._refresh_parser(waitfor=self.__waitfor)

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapability: No filter queries to update
        """
        elem = self.page.query_selector("#button-update")
        if elem is None:
            raise fangraphs.exceptions.FilterUpdateIncapability()
        self._close_ad()
        elem.click()
        self._refresh_parser(waitfor=self.__waitfor)

    def list_filter_groups(self):
        """
        Lists the possible groups of filter queries which can be used

        :return: Names of the groups of filter queries
        :rtype: list
        """
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        groups = [e.getText() for e in elems]
        return groups

    def configure_filter_group(self, group="Show All"):
        """
        Configures the available filters to a specified group of filters

        :param group: The name of the group of filters
        """
        selector = ".fgBin.splits-bin-controller div"
        elems = self.soup.select(selector)
        options = [e.getText() for e in elems]
        try:
            index = options.index(group)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterGroup(group) from err
        self._close_ad()
        elem = self.page.query_selector_all(selector)[index]
        elem.click()

    def reset_filters(self):
        """
        Resets filters to the original option(s).
        This does not affect the following filter queries:

        - ``group``
        - ``stat``
        - ``type``
        - ``groupby``
        - ``preset_range``
        - ``auto_pt``
        - ``split_teams``
        """
        elem = self.page.query_selector(
            "#stack-buttons .fgButton.small:nth-last-child(1)"
        )
        if elem is None:
            return
        self._close_ad()
        elem.click()

    @classmethod
    def list_quick_splits(cls):
        """
        Lists all the quick splits which can be used.
        Quick splits allow for the configuration of multiple filter queries at once.

        :return: All available quick splits
        :rtype: list
        """
        return list(cls.__quick_splits)

    def set_to_quick_split(self, quick_split: str, autoupdate=True):
        """
        Invokes the configuration of a quick split.
        All filter queries affected by :py:meth:`reset_filters` are reset prior to configuration.
        This action is performed by the FanGraphs API and cannot be prevented.

        :param quick_split: The quick split to invoke
        :param autoupdate: If ``True``, :py:meth:`reset_filters` will be called
        :raises FanGraphs.exceptions.InvalidQuickSplitsException: Invalid argument ``quick_split``
        """
        quick_split = quick_split.lower()
        try:
            selector = self.__quick_splits[quick_split]
        except ValueError as err:
            raise fangraphs.exceptions.InvalidQuickSplit(quick_split) from err
        self._close_ad()
        self.page.click(selector)
        if autoupdate:
            self.update()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self.export_data(".data-export", path)
