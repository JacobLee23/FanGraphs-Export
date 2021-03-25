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
from FanGraphs.selectors import leaders_sel


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
            raise FanGraphs.exceptions.UnknownBrowser(browser.lower())
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

    __selections = leaders_sel.mll.selections
    __dropdowns = leaders_sel.mll.dropdowns
    __dropdown_options = leaders_sel.mll.dropdown_options
    __checkboxes = leaders_sel.mll.checkboxes
    __buttons = leaders_sel.mll.buttons

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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
        self._close_ad()
        if query in self.__selections:
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__checkboxes:
            self.__configure_checkbox(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option)
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
    __selections = leaders_sel.splits.selections
    __dropdowns = leaders_sel.splits.dropdowns
    __splits = leaders_sel.splits.splits
    __quick_splits = leaders_sel.splits.quick_splits
    __switches = leaders_sel.splits.switches
    __waitfor = leaders_sel.splits.waitfor

    address = "https://fangraphs.com/leaders/splits-leaderboards"

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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        elif query in self.__splits:
            self.__configure_split(query, option)
        elif query in self.__switches:
            self.__configure_switch(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
        if autoupdate:
            self.update()
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.hover(self.__splits[query])
        elem = self.page.query_selector_all(f"{self.__splits[query]} ul li")[index]
        elem.click()

    def __configure_switch(self, query: str, option: str):
        """
        Configures a switch-class filter query to an option.

        :param query: The switch-class filter query to be configured
        :param option: The option to configure the filter query to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        if option not in options:
            raise FanGraphs.exceptions.InvalidFilterOption(query, option)
        if option != self.current_option(query)[0].title():
            self.page.click(self.__switches[query])

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapability: No filter queries to update
        """
        selector = "#button-update"
        elem = self.page.query_selector(selector)
        if elem is None:
            raise FanGraphs.exceptions.FilterUpdateIncapability()
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
        :raises FanGraphs.exceptions.InvalidQuickSplitsException: Invalid argument ``quick_split``
        """
        quick_split = quick_split.lower()
        try:
            selector = self.__quick_splits[quick_split]
        except ValueError as err:
            raise FanGraphs.exceptions.InvalidQuickSplitException(quick_split) from err
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
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click(".data-export")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class SeasonStatGrid(ScrapingUtilities):
    """
    Parses the FanGraphs Season Stat Grid webpage.

    .. py:attribute:: address
        The base URL address of the Season Stat Grid page.

        :type: str
        :value: https://fangraphs.com/season-stat-grid
    """
    __selections = leaders_sel.ssg.selections
    __dropdowns = leaders_sel.ssg.dropdowns
    __waitfor = leaders_sel.ssg.waitfor

    address = "https://fangraphs.com/leaders/season-stat-grid"

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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            self.__configure_selection(query, option)
        elif query in self.__dropdowns:
            self.__configure_dropdown(query, option)
        else:
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
        self._refresh_parser(waitfor=self.__waitfor)

    def __configure_selection(self, query: str, option: str):
        """
        Configures a selection-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

    def __configure_dropdown(self, query: str, option: str):
        """
        Configures a dropdown-class filter query to a specified option.

        :param query: The filter query
        :param option: The option to configure ``query`` to
        :raises FanGraphs.exceptions.InvalidFilterOption: Invalid argument ``option``
        """
        options = self.list_options(query)
        try:
            index = options.index(option)
        except ValueError as err:
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
            for _ in range(0, total_pages):
                self._write_table_rows(writer)
                self.page.click(
                    ".table-page-control:nth-last-child(1) > .next"
                )
                self._refresh_parser(waitfor=self.__waitfor)


class GameSpanLeaderboards(ScrapingUtilities):
    """
    Parses the FanGraphs 60-Game Span Leaderboards

    .. py:attribute:: address

        The base URL address of the 60-Game Span Leaderboards page

        :type: str
        :value: https://fangraphs.com/leaders/special/60-game-span
    """
    __selections = leaders_sel.gsl.selections
    __dropdowns = leaders_sel.gsl.dropdowns
    __waitfor = leaders_sel.gsl.waitfor

    address = "https://fangraphs.com/leaders/special/60-game-span"

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
            elems = self.soup.select(f"{self.__dropdowns[query]} > div > a")
            options = [e.getText() for e in elems]
        else:
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
        else:
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
        self.page.click(self.__selections[query][index])

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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click(".data-export")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)


class InternationalLeaderboards(ScrapingUtilities):
    """
    Parses the FanGraphs KBO Leaderboards page

    .. py:attribute:: address

        The base URL address for the FanGraphs KBO Leaderboards page.

        :type: str
        :value: https://www.fangraphs.com/leaders/international
    """
    __selections = leaders_sel.intl.selections
    __dropdowns = leaders_sel.intl.dropdowns
    __checkboxes = leaders_sel.intl.checkboxes
    __waitfor = leaders_sel.intl.waitfor

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

        :return:
        """
        queries = []
        queries.extend(cls.__selections)
        queries.extend(cls.__dropdowns)
        queries.extend(cls.__checkboxes)
        return queries

    def list_options(self, query: str):
        """

        :param query:
        :return:
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
        return option


class WARLeaderboards(ScrapingUtilities):
    """
    Parses the FanGraphs WAR Leaderboards page

    .. py:attribute:: address

        The base URL address for the FanGraphs WAR Leaderboards page.

        :type: str
        :value: https://fangraphs.com/warleaders.aspx
    """
    __dropdowns = leaders_sel.war.dropdowns
    __dropdown_options = leaders_sel.war.dropdown_options
    __waitfor = leaders_sel.war.waitfor

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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterQuery(query)
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
            raise FanGraphs.exceptions.InvalidFilterOption(query, option) from err
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
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click("#WARBoard1_cmdCSV")
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)
