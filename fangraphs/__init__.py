#! python3
# FanGraphs/__init__.py

"""
Subpackage for scraping the FanGraphs **Leaders** pages.
"""

import os

import bs4
from playwright.sync_api import sync_playwright


class ScrapingUtilities:
    """
    Manages the various objects used for scraping the FanGraphs webpages.
    Intializes and manages ``Playwright`` browsers and pages.
    Intializes and manages ``bs4.BeautifulSoup`` objects.
    """
    def __init__(self, address, *, selector_mod):
        """
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
        self.waitfor = selector_mod.waitfor
        self.export_data = selector_mod.export_data
        os.makedirs("out", exist_ok=True)

        self.__play = None
        self.__browser = None
        self.page = None

        self.soup = None

    def _browser_init(self):
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch(
            downloads_path=os.path.abspath("out")
        )
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self._refresh_parser()

    def _refresh_parser(self):
        """
        Re-initializes the ``bs4.BeautifulSoup`` object stored in :py:attr:`soup`.
        """
        if self.waitfor:
            self.page.wait_for_selector(self.waitfor)
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

    @staticmethod
    def list_queries():
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        raise NotImplementedError

    @staticmethod
    def list_options(query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        raise NotImplementedError

    @staticmethod
    def current_option(query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        raise NotImplementedError

    @staticmethod
    def configure(query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        raise NotImplementedError

    def export(self, *, path):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The file will be saved to the filepath determined by ``path``.

        :param path: The path to save the exported data to
        """
        self._close_ad()
        with self.page.expect_download() as down_info:
            self.page.click(self.export_data)
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)

    def reset(self):
        """
        Navigates :py:attr:`page` to :py:attr:`address`.
        """
        self.page.goto(self.address, timeout=0)
        self._refresh_parser()

    def quit(self):
        """
        Terminates the ``Playwright`` browser and context manager.
        """
        self.__browser.close()
        self.__play.stop()
