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


class MajorLeagueLeaderboards:
    """
    Parses the FanGraphs Major League Leaderboards page.
    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`

    .. py:attribute:: address
        The base URL address of the Major League Leaderboards page

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

        .. py:attribute:: page
            The generated synchronous ``Playwright`` page for browser automation.

            :type: playwright.sync_api._generated.Page

        .. py:attribute:: soup
            The ``BeautifulSoup4`` HTML parser for scraping the webpage.

            :type: bs4.BeautifulSoup
        """
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
        self.page.goto(self.address)

        self.soup = None
        self.__refresh_parser()

    def __refresh_parser(self):
        """
        Re-initializes the ``bs4.BeautifulSoup`` object stored in :py:attr:`soup`.
        Called when a page refresh is expected
        """
        self.soup = bs4.BeautifulSoup(
            self.page.content(), features="lxml"
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
        queries.extend(list(cls.__checkboxes))
        return queries

    def list_options(self, query: str):
        """
        Lists the possible options which the filter query can be configured to.

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
        Retrieves the option which the filter query is currently set to.

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
        Configures a filter query ``query`` to a specified option ``option``.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, any form submission buttons attached to the filter query will be clicked
        :raises FanGraphs.exceptions.InvalidFilterQueryException: Argument ``query`` is invalid
        """
        query, option = query.lower(), str(option).lower()
        if query not in self.list_queries():
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        self.__close_ad()
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
        self.__refresh_parser()

    def __configure_selection(self, query, option):
        """
        Configures a selection-class filter query ``query`` to an option ``option``

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
        Configures a dropdown-class filter query ``query`` to an option ``option``

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
        Configures a checkbox-class filter query ``query`` to an option ``option``.

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

    def __close_ad(self):
        """
        Closes the ad which may interfere with clicking other page elements.
        """
        elem = self.page.query_selector(".ezmob-footer-close")
        if elem:
            elem.click()

    def quit(self):
        """
        Terminates the underlying ``Playwright`` browser context.
        """
        self.__browser.close()
        self.__play.stop()

    def reset(self):
        """
        Navigates to the webpage corresponding to :py:attr:`address`.
        """
        self.page.goto(self.address)
        self.__refresh_parser()

    def export(self, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        self.__close_ad()
        with self.page.expect_download() as down_info:
            self.page.click("#LeaderBoard1_cmdCSV")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class SplitsLeaderboards:
    """
    Parses the FanGraphs Splits Leaderboards page.

    .. py:attribute:: address
        The base URL address which corresponds to the Splits Leaderboards page

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

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)

        .. py:attribute:: page
            The generated synchronous ``playwright`` page for browser automation.

            :type: playwright.sync_api._generated.Page

        .. py:attribute:: soup
            The ``BeautifulSoup4`` HTML parser for scraping the webpage.

            :type: bs4.BeautifulSoup
        """
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
        self.__browser = browser_ctx.launch()
        self.page = self.__browser.new_page()
        self.page.goto(self.address, timeout=0)

        self.soup = None
        self.__refresh_parser()

        self.configure_filter_group("Show All")
        self.configure("auto_pt", "False", autoupdate=True)

    def __refresh_parser(self):
        """
        Re-initializes the ``bs4.BeautifulSoup`` object stored in :py:attr:`soup`.
        Called when a page refresh is expected
        """
        self.soup = bs4.BeautifulSoup(
            self.page.content(), features="lxml"
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
        Lists the possible options which the filter query can be configured to.

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
        Retrieves the option(s) which the filter query is currently set to.
        *Note: Some dropdown- and split-class filter queries can be configured to multiple options.
        Since this is the case, a list is returned, even though there may only be one option.*

        :param query: The filter query being retrieved of its current option
        :return: The option(s) which the filter query is currently set to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        options = []
        if query in self.__selections:
            for sel in self.__selections[query]:
                elem = self.soup.select(sel)[0]
                if "isActive" in elem.get("class"):
                    options = [elem.getText()]
                    break
        elif query in self.__dropdowns:
            elems = self.soup.select(
                f"{self.__dropdowns[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    options.append(elem.getText())
        elif query in self.__splits:
            elems = self.soup.select(
                f"{self.__splits[query]} ul li"
            )
            for elem in elems:
                if "highlight-selection" in elem.get("class"):
                    options.append(elem.getText())
        elif query in self.__switches:
            elem = self.soup.select(self.__switches[query])
            options = ["True" if "isActive" in elem[0].get("class") else "False"]
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        return options

    def configure(self, query: str, option: str, *, autoupdate=False):
        """
        Configures a filter query ``query`` to a specified option ``option``.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :param autoupdate: If ``True``, :py:meth:`update` will be called following configuration
        :raises FanGraphs.exceptions.InvalidFilterQueryException: Argument ``query`` is invalid
        """
        self.__close_ad()
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
        self.__refresh_parser()

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query ``query`` to an option ``option``

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
        Configures a dropdown-class filter query ``query`` to an option ``option``.

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
        Configures a split-class filter query ``query`` to an option ``option``.
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

    def __configure_switch(self, query, option):
        """
        Configures a switch-class filter query ``query`` to an option ``option``.

        :param query: The switch-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOptionException: Argument ``option`` is invalid
        """
        options = self.list_options(query)
        if option not in options:
            raise FanGraphs.exceptions.InvalidFilterOptionException(query, option)
        if option != self.current_option(query)[0].title():
            self.page.click(self.__switches[query])

    def __close_ad(self):
        """
        Closes the ad which may interfere with clicking other page elements.
        """
        elem = self.page.query_selector(".ezmob-footer-close")
        if elem and elem.is_visible():
            elem.click()

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
        self.__close_ad()
        elem.click()
        self.__refresh_parser()

    def list_filter_groups(self):
        """
        Lists the possible groups of filter queries which can be used

        :return: Names of the groups of filter queries
        :rtype: list
        """
        selector = ".fgBin.splits-bin-controller div"
        elems = self.soup.select(selector)
        groups = [e.getText() for e in elems]
        return groups

    def configure_filter_group(self, group="Show All"):
        """
        Configures the available filters to the specified group of filters

        :param group: The name of the group of filters
        """
        selector = ".fgBin.splits-bin-controller div"
        elems = self.soup.select(selector)
        options = [e.getText() for e in elems]
        try:
            index = options.index(group)
        except ValueError:
            raise Exception
        self.__close_ad()
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
        self.__close_ad()
        elem.click()

    def list_quick_splits(self):
        """
        Lists all the quick splits which can be used.
        Quick splits allow for the configuration of multiple filter queries at once.

        :return: All available quick splits
        :rtype: list
        """
        return list(self.__quick_splits)

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
        self.__close_ad()
        self.page.click(selector)
        if autoupdate:
            self.update()

    def export(self, path="", *, size="Infinity", sortby="", reverse=False):
        """
        Scrapes and saves the data from the table of the current leaderboards
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *out/%d.%m.%y %H.%M.%S.csv*

        *Note: This is a 'manual' export of the data.
        In other words, the data is scraped from the table.
        This is unlike other forms of export where a button is clicked.
        Thus, there will be no record of a download when the data is exported.*

        :param path: The path to save the exported file to
        :param size: The maximum number of rows of the table to export
        :param sortby: The table header to sort the data by
        :param reverse: If ``True``, the organization of the data will be reversed
        :return:
        """
        self.page.hover(".data-export")
        self.__close_ad()
        self.__expand_table(size=size)
        if sortby:
            self.__sortby(sortby.title(), reverse=reverse)
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with open(os.path.join("out", path), "w", newline="") as file:
            writer = csv.writer(file)
            self.__write_table_headers(writer)
            self.__write_table_rows(writer)

    def __expand_table(self, *, size="Infinity"):
        """
        Expands the data table to the appropriate number of rows

        :param size: The maximum number of rows the table should have.
        The number of rows is preset (30, 50, 100, 200, Infinity).
        """
        selector = ".table-page-control:nth-child(3) select"
        dropdown = self.page.query_selector(selector)
        dropdown.click()
        elems = self.soup.select(f"{selector} option")
        options = [e.getText() for e in elems]
        size = "Infinity" if size not in options else size
        index = options.index(size)
        option = self.page.query_selector_all(f"{selector} option")[index]
        option.click()

    def __sortby(self, sortby, *, reverse=False):
        """
        Sorts the data by the appropriate table header.

        :param sortby: The table header to sort the data by
        :param reverse: If ``True``, the organizatino of the data will be reversed
        """
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        options = [e.getText() for e in elems]
        index = options.index(sortby)
        option = self.page.query_selector_all(selector)[index]
        option.click()
        if reverse:
            option.click()

    def __write_table_headers(self, writer: csv.writer):
        """
        Writes the data table headers to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        headers = [e.getText() for e in elems]
        writer.writerow(headers)

    def __write_table_rows(self, writer: csv.writer):
        """
        Iterates through the rows of the data table and writes the data in each row to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        selector = ".table-scroll tbody tr"
        row_elems = self.soup.select(selector)
        for row in row_elems:
            elems = row.select("td")
            items = [e.getText() for e in elems]
            writer.writerow(items)

    def reset(self):
        """
        Navigates to the webpage corresponding to :py:attr:`address`.
        """
        self.page.goto(self.address)
        self.__refresh_parser()

    def quit(self):
        """
        Terminates the underlying ``playwright`` browser context.
        """
        self.__browser.close()
        self.__play.stop()


class SeasonStatGrid:
    """
    Scrapes the FanGraphs Season Stat Grid webpage.

    .. py:attribute:: address
        The base URL address of the Season Stat Grid page

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

    def __init__(self, *, browser="chromium"):
        """
        :param browser: The name of the browser to use (Chromium, Firefox, WebKit)

        .. py:attribute:: page
            The generated synchronous ``playwright`` page for browser automation.

            :type: playwright.sync_api._generated.Page

        .. py:attribute:: soup
            The ``BeautifulSoup4`` HTML parser for scraping the webpage.

            :type: bs4.BeautifulSoup
        """
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
        self.__browser = browser_ctx.launch()
        self.page = self.__browser.new_page()
        self.page.goto(self.address)

        self.soup = None
        self.__refresh_parsers()

    def __refresh_parsers(self):
        """
        Re-initializes the ``bs4.BeautifulSoup`` object stored in :py:attr:`soup`.
        Called when a page refresh is expected
        """
        self.soup = bs4.BeautifulSoup(
            self.page.content(), features="lxml"
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
        Lists the possible options which the filter query can be configured to.

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
        Retrieves the option which the filter query is currently configured to.

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
        Configures the filter query to the specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Argument ``query`` is invalid
        :raises FanGraphs.exceptions.InvalidFilterOption: Filter ``query`` cannot be configured to ``option``
        """
        query = query.lower()
        self.__close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQueryException(query)
        self.__refresh_parsers()

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

    def __close_ad(self):
        """
        Closes the ad which may interfere with interactions with other page elements
        """
        elem = self.page.query_selector(".ezmob-footer-close")
        if elem and elem.is_visible():
            elem.click()

    def export(self, path="", *, size="Infinity", sortby="Name", reverse=False):
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
        :param size: The maximum number of rows of the table to export
        :param sortby: The table header to sort the data by
        :param reverse: If ``True``, the organization of the data will be reversed
        """
        self.__close_ad()
        self.__expand_table(size=size)
        self.__sortby(sortby.title(), reverse=reverse)
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with open(os.path.join("out", path), "w", newline="") as file:
            writer = csv.writer(file)
            self.__write_table_headers(writer)
            self.__write_table_rows(writer)

    def __expand_table(self, *, size="Infinity"):
        """
        Expands the data table to the appropriate number of rows

        :param size: The maximum number of rows the table should have.
        The number of rows is preset (30, 50, 100, 200, Infinity).
        """
        selector = ".table-page-control:nth-child(3) select"
        dropdown = self.page.query_selector(selector)
        dropdown.click()
        elems = self.soup.select(f"{selector} option")
        options = [e.getText() for e in elems]
        size = "Infinity" if size not in options else size
        index = options.index(size)
        option = self.page.query_selector_all(f"{selector} option")[index]
        option.click()

    def __sortby(self, sortby, *, reverse=False):
        """
        Sorts the data by the appropriate table header.

        :param sortby: The table header to sort the data by
        :param reverse: If ``True``, the organizatino of the data will be reversed
        """
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        options = [e.getText() for e in elems]
        index = options.index(sortby)
        option = self.page.query_selector_all(selector)[index]
        option.click()
        if reverse:
            option.click()

    def __write_table_headers(self, writer: csv.writer):
        """
        Writes the data table headers to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        headers = [e.getText() for e in elems]
        writer.writerow(headers)

    def __write_table_rows(self, writer: csv.writer):
        """
        Iterates through the rows of the data table and writes the data in each row to the CSV file.

        :param writer: The ``csv.writer`` object
        """
        selector = ".table-scroll tbody tr"
        row_elems = self.soup.select(selector)
        for row in row_elems:
            elems = row.select("td")
            items = [e.getText() for e in elems]
            writer.writerow(items)

    def reset(self):
        """
        Navigates to the webpage corresponding to :py:attr:`address`.
        """
        self.page.goto(self.address)
        self.__refresh_parsers()

    def quit(self):
        """
        Terminates the underlying ``playwright`` browser context.
        """
        self.__browser.close()
        self.__play.stop()


class GameSpanLeaderboards:

    def __init__(self):
        pass


class InternationalLeaderboards:

    def __init__(self):
        pass


class WARLeaderboards:

    def __init__(self):
        pass
