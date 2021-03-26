#! python3
# FanGraphs/utilities.py

"""
Helper module with web scraping utilities.
"""

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

    def export_data(self, selector: str, path=""):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param selector: The CSS selector of the **Export Data** button
        :param path: The path to save the exported data to
        """
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        with self.page.expect_download() as down_info:
            self.page.click(selector)
        download = down_info.value
        download_path = download.path()
        os.rename(download_path, path)

    def reset(self, *, waitfor=""):
        """
        Navigates :py:attr:`page` to :py:attr:`address`.

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
