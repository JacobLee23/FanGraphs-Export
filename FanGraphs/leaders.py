#! python3
# FanGraphs/leaders.py

"""
Web scraper for the **Leaders** tab of the `FanGraphs website`_.
Each page which is covered has its own class for scraping it.
Below are each of the covered pages with the corresponding class:

- `Major League Leaderboards`_: :py:class:`MajorLeagueLeaderboards`
- `Splits Leaderboards`_: :py:class:`SplitsLeaderboards`
- `Season Stat Grid`_: :py:class:`SeasonStatGrid`
- `60-Game Span Leaderboards`_: :py:class:`GameSpanLeaderboards`
- `KBO Leaders`_: :py:class:`InternationalLeaderboards`
- `Combined WAR Leaderboards`_: :py:class:`WARLeaderboards`

.. _FanGraphs website: https://fangraphs.com
.. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
.. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
.. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
.. _60-Game Span Leaderboards: https://www.fangraphs.com/leaders/special/60-game-span
.. _KBO Leaders: https://www.fangraphs.com/leaders/international
.. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
================================================================================
"""

import csv
import datetime
import os

import bs4
from playwright.sync_api import sync_playwright

import FanGraphs.exceptions


class ScrapingUtilities:
    """
    Manages the various objects used for scraping the FanGraphs webpages.

    Intializes and manages ``Playwright`` browsers and pages.
    Intializes and manages ``bs4.BeautifulSoup`` objects.
    """
    def __init__(self, browser, address):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        :param address: The base URL address of the FanGraphs page

        .. py:attribute:: address

            The base URL address of the FanGraphs page

            :type: str

        .. py:attribute:: page
            The generated synchronous ``Playwright`` page for browser automation.

            :type: playwright.sync_api._generated.Page

        .. py:attribute:: soup
            The ``BeautifulSoup4`` HTML parser for scraping the webpage.

            :type: bs4.BeautifulSoup
        """
        self.address = address
        os.makedirs("out", exist_ok=True)

        self.__play = sync_playwright().start()
        browsers = {
            "chromium": self.__play.chromium,
            "firefox": self.__play.firefox,
            "webkit": self.__play.webkit
        }
        browser_ctx = browsers.get(browser.lower())
        if browser_ctx is None:
            raise FanGraphs.exceptions.UnknownBrowserException(browser.lower())
        self.__browser = browser_ctx.launch(
            downloads_path=os.path.abspath("out")
        )
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self.soup = None

    def _refresh_parser(self, *, waitfor=""):
        """
        Re-initializes the ``bs4.BeautifulSoup`` object stored in :py:attr:`soup`.
        """
        if waitfor:
            self.page.wait_for_selector(waitfor)
        self.soup = bs4.BeautifulSoup(
            self.page.content(), features="lxml"
        )

    def _close_ad(self):
        """
        Closes the ad which may interfere with clicking other page elements.
        """
        elem = self.page.query_selector(".ezmob-footer-close")
        if self.soup.select("#ezmob-wrapper > div[style='display: none;']"):
            return
        if elem:
            elem.click()

    def reset(self, *, waitfor=""):
        """
        Navigates to :py:attr:`page` to :py:attr:`address`.

        :param waitfor: If specified, the CSS of the selector to wait for.
        The wait will occur after the page has navigated to the webpage and before the parser is refreshed.
        See `here`_ for more information.

        .. _here: https://playwright.dev/python/docs/api/class-page/#pagewait_for_selectorselector-kwargs
        """
        self.page.goto(self.address, timeout=0)
        self._refresh_parser(waitfor=waitfor)

    def quit(self):
        """
        Terminates the ``Playwright`` browser and context manager.
        """
        self.__browser.close()
        self.__play.stop()


class MajorLeagueLeaderboards(ScrapingUtilities):
    """
    Parses the FanGraphs Major League Leaderboards page.
    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`

    .. py:attribute:: address
        The base URL address of the Major League Leaderboards page.

        :type: str
        :value: https://fangraphs.com/leaders.aspx
    """

    __selections = {
        "group": "#LeaderBoard1_tsGroup",
        "stat": "#LeaderBoard1_tsStats",
        "position": "#LeaderBoard1_tsPosition",
        "type": "#LeaderBoard1_tsType"
    }
    __dropdowns = {
        "league": "#LeaderBoard1_rcbLeague_Input",
        "team": "#LeaderBoard1_rcbTeam_Input",
        "single_season": "#LeaderBoard1_rcbSeason_Input",
        "split": "#LeaderBoard1_rcbMonth_Input",
        "min_pa": "#LeaderBoard1_rcbMin_Input",
        "season1": "#LeaderBoard1_rcbSeason1_Input",
        "season2": "#LeaderBoard1_rcbSeason2_Input",
        "age1": "#LeaderBoard1_rcbAge1_Input",
        "age2": "#LeaderBoard1_rcbAge2_Input"
    }
    __dropdown_options = {
        "league": "#LeaderBoard1_rcbLeague_DropDown",
        "team": "#LeaderBoard1_rcbTeam_DropDown",
        "single_season": "#LeaderBoard1_rcbSeason_DropDown",
        "split": "#LeaderBoard1_rcbMonth_DropDown",
        "min_pa": "#LeaderBoard1_rcbMin_DropDown",
        "season1": "#LeaderBoard1_rcbSeason1_DropDown",
        "season2": "#LeaderBoard1_rcbSeason2_DropDown",
        "age1": "#LeaderBoard1_rcbAge1_DropDown",
        "age2": "#LeaderBoard1_rcbAge2_DropDown"
    }
    __checkboxes = {
        "split_teams": "#LeaderBoard1_cbTeams",
        "active_roster": "#LeaderBoard1_cbActive",
        "hof": "#LeaderBoard1_cbHOF",
        "split_seasons": "#LeaderBoard1_cbSeason",
        "rookies": "#LeaderBoard1_cbRookie"
    }
    __buttons = {
        "season1": "#LeaderBoard1_btnMSeason",
        "season2": "#LeaderBoard1_btnMSeason",
        "age1": "#LeaderBoard1_cmdAge",
        "age2": "#LeaderBoard1_cmdAge"
    }
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
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
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
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
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
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=True):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, any form submission buttons attached to the filter query will be clicked
        :raises FanGraphs.exceptions.InvalidFilterQueryException: Argument ``query`` is invalid
        """
        query, option = query.lower(), str(option).lower()
        if query not in self.list_queries():
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        if query in self.__buttons and autoupdate:
            self.__click_button(query)
        self._refresh_parser()

    def __configure_selection(self, query, option):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
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
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = [o.lower() for o in self.list_options(query)]
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
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
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
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
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click("#LeaderBoard1_cmdCSV")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class SplitsLeaderboards(ScrapingUtilities):
    """
    Parses the FanGraphs Splits Leaderboards page.

    .. py:attribute:: address
        The base URL address which corresponds to the Splits Leaderboards page.

        :type: str
        :value: https://fangraphs.com/leaders/splits-leaderboards
    """
    __selections = {
        "group": [
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(1)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(2)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(3)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(4)"
        ],
        "stat": [
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(6)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(7)"
        ],
        "type": [
            "#root-buttons-stats > div:nth-child(1)",
            "#root-buttons-stats > div:nth-child(2)",
            "#root-buttons-stats > div:nth-child(3)"
        ]
    }
    __dropdowns = {
        "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
        "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
        "groupby": ".fg-dropdown.group-by"
    }
    __splits = {
        "handedness": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "home_away": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(2)",
        "batted_ball": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(3)",
        "situation": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(4)",
        "count": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(5)",
        "batting_order": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "position": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(2)",
        "inning": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(3)",
        "leverage": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(4)",
        "shifts": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(5)",
        "team": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "opponent": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(2)",
    }
    __quick_splits = {
        "batting_home": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(1)",
        "batting_away": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(2)",
        "vs_lhp": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(1)",
        "vs_lhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(2)",
        "vs_lhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(3)",
        "vs_lhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(4)",
        "vs_lhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(5)",
        "vs_rhp": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(2)",
        "vs_rhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(3)",
        "vs_rhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(4)",
        "vs_rhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(5)",
        "pitching_as_sp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(1)",
        "pitching_as_rp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(2)",
        "pitching_home": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(1)",
        "pitching_away": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(2)",
        "vs_lhh": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(1)",
        "vs_lhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(2)",
        "vs_lhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(3)",
        "vs_lhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(4)",
        "vs_lhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(5)",
        "vs_rhh": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)"
    }
    __switches = {
        "split_teams": "#stack-buttons > div:nth-child(2)",
        "auto_pt": "#stack-buttons > div:nth-child(3)"
    }

    address = "https://fangraphs.com/leaders/splits-leaderboards"
    __waitfor = ".fg-data-grid.undefined"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

        self.configure_filter_group("Show All")
        self.configure("auto_pt", "False", autoupdate=True)

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
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            selector = f"{self.__dropdowns[query]} ul li"
            elems = self.soup.select(selector)
            options = [e.getText() for e in elems]
        elif query in self.__splits:
            selector = f"{self.__splits[query]} ul li"
            elems = self.soup.select(selector)
            options = [e.getText() for e in elems]
        elif query in self.__switches:
            options = ["True", "False"]
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
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
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        option = []
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "isActive" in elem.get("class"):
                    option = elem.getText()
                    break
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    option.append(elem.getText())
        elif query in self.__splits:
            elems = self.soup.select(
                f"{self.__splits[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    option.append(elem.getText())
        elif query in self.__switches:
            elem = self.soup.select(self.__switches[query])
            option = "True" if "isActive" in elem[0].get("class") else "False"
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return option

    def configure(self, query: str, option: str, *, autoupdate=False):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, :py:meth:`update` will be called following configuration
        :raises FanGraphs.exceptions.InvalidFilterQueryException: Argument ``query`` is invalid
        """
        self._close_ad()
        query = query.lower()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__splits:
            self.__configure_split(query, option)
        elif query in self.__switches:
            self.__configure_switch(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        if autoupdate:
            self.update()
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.hover(self.__dropdowns[query])
        elem = self.page.query_selector_all(f"{self.__dropdowns[query]} ul li")[index]
        elem.click()

    def __configure_split(self, query: str, option: str):
        """
        Configures a split-class filter query to an option.
        Split-class filter queries are separated from dropdown-class filter queries.
        This is solely because of the CSS selectors used.

        :param query: The split-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.hover(self.__splits[query])
        elem = self.page.query_selector_all(f"{self.__splits[query]} ul li")[index]
        elem.click()

    def __configure_switch(self, query: str, option: str):
        """
        Configures a switch-class filter query to an option.

        :param query: The switch-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        if option not in options:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        if option != self.current_option(query)[0].title():
            self.page.click(self.__switches[query])

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapabilityWarning: No filter query configurations to update
        """
        selector = "#button-update"
        elem = self.page.query_selector(selector)
        if elem is None:
            raise FanGraphs.exceptions.FilterUpdateIncapabilityWarning()
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
        except ValueError:
            raise Exception
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
        selector = "#stack-buttons div[class='fgButton small']:nth-last-child(1)"
        elem = self.page.query_selector(selector)
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

    def configure_quick_split(self, quick_split: str, autoupdate=True):
        """
        Invokes the configuration of a quick split.
        All filter queries affected by :py:meth:`reset_filters` are reset prior to configuration.
        This action is performed by the FanGraphs API and cannot be prevented.

        :param quick_split: The quick split to invoke
        :param autoupdate: If ``True``, :py:meth:`reset_filters` will be called
        :raises FanGraphs.exceptions.InvalidQuickSplitsException: Argument ``quick_split`` if invalid
        """
        quick_split = quick_split.lower()
        try:
            selector = self.__quick_splits[quick_split]
        except KeyError:
            raise FanGraphs.exceptions.InvalidQuickSplitException(quick_split)
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
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click(".data-export")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class SeasonStatGrid(ScrapingUtilities):
    """
    Scrapes the FanGraphs Season Stat Grid webpage.

    .. py:attribute:: address
        The base URL address of the Season Stat Grid page.

        :type: str
        :value: https://fangraphs.com/season-stat-grid
    """

    __selections = {
        "stat": [
            "div[class*='fgButton button-green']:nth-child(1)",
            "div[class*='fgButton button-green']:nth-child(2)"
        ],
        "type": [
            "div[class*='fgButton button-green']:nth-child(4)",
            "div[class*='fgButton button-green']:nth-child(5)",
            "div[class*='fgButton button-green']:nth-child(6)"
        ]
    }
    __dropdowns = {
        "start_season": ".row-season > div:nth-child(2)",
        "end_season": ".row-season > div:nth-child(4)",
        "popular": ".season-grid-controls-dropdown-row-stats > div:nth-child(1)",
        "standard": ".season-grid-controls-dropdown-row-stats > div:nth-child(2)",
        "advanced": ".season-grid-controls-dropdown-row-stats > div:nth-child(3)",
        "statcast": ".season-grid-controls-dropdown-row-stats > div:nth-child(4)",
        "batted_ball": ".season-grid-controls-dropdown-row-stats > div:nth-child(5)",
        "win_probability": ".season-grid-controls-dropdown-row-stats > div:nth-child(6)",
        "pitch_type": ".season-grid-controls-dropdown-row-stats > div:nth-child(7)",
        "plate_discipline": ".season-grid-controls-dropdown-row-stats > div:nth-child(8)",
        "value": ".season-grid-controls-dropdown-row-stats > div:nth-child(9)"
    }
    address = "https://fangraphs.com/leaders/season-stat-grid"
    __waitfor = ".fg-data-grid.undefined"

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(browser, self.address)
        self.reset(waitfor=self.__waitfor)

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
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} li"
            )
            options = [e.getText() for e in elems]
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
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
            selector = "div[class='fgButton button-green active isActive']"
            elems = self.soup.select(selector)
            option = {
                "stat": elems[0].getText(), "type": elems[1].getText()
            }[query]
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} li[class$='highlight-selection']"
            )
            option = elems[0].getText() if elems else "None"
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        :raises FanGraphs.exceptions.InvalidFilterOption: Filter ``query`` cannot be configured to ``option``
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Filter ``query`` cannot be configured to ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Filter ``query`` cannot be configured to ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.hover(self.__dropdowns[query])
        elem = self.page.query_selector_all(f"{self.__dropdowns[query]} ul li")[index]
        elem.click()

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
            for page in range(0, total_pages):
                self._write_table_rows(writer)
                self.page.click(
                    ".table-page-control:nth-last-child(1) > .next"
                )
                self._refresh_parser(waitfor=self.__waitfor)


class GameSpanLeaderboards(ScrapingUtilities):
    """
    Scrape the FanGraphs 60-Game Span Leaderboards

    .. py:attribute:: address

        The base URL address of the 60-Game Span Leaderboards page

        :type: str
        :value: https://fangraphs.com/leaders/special/60-game-span
    """
    __selections = {
        "stat": [
            ".controls-stats > .fgButton:nth-child(1)",
            ".controls-stats > .fgButton:nth-child(2)"
        ],
        "type": [
            ".controls-board-view > .fgButton:nth-child(1)",
            ".controls-board-view > .fgButton:nth-child(2)",
            ".controls-board-view > .fgButton:nth-child(3)"
        ]
    }
    __dropdowns = {
        "min_pa": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
        "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
        "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
        "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
        "determine": ".controls-stats.stat-determined > div:nth-child(1) > .fg-selection-box__selection"
    }
    address = "https://fangraphs.com/leaders/special/60-game-span"
    __waitfor = ".fg-data-grid.table-type"

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
        queries.extend(list(cls.__selections))
        queries.extend(list(cls.__dropdowns))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__selections:
            elems = [
                self.soup.select(s)[0]
                for s in self.__selections[query]
            ]
            options = [e.getText() for e in elems]
        elif query in self.__dropdowns:
            elems = self.soup.select(f"{self.__dropdowns[query]} > div > a")
            options = [e.getText() for e in elems]
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return options

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
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
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return option

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQueryException: Argument ``query`` is invalid
        """
        query = query.lower()
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to an option.

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to an option.

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        self.page.click(self.__dropdowns[query])
        elem = self.page.query_selector_all(
            f"{self.__dropdowns[query]} > div > a"
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
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click(".data-export")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class InternationalLeaderboards:

    def __init__(self):
        pass


class WARLeaderboards:

    def __init__(self):
        pass
