#! python3
# FanGraphs/__init__.py

"""
Subpackage for scraping the FanGraphs **Leaders** pages.
"""

import datetime as dt
import os

import bs4
from playwright.sync_api import sync_playwright


FORMAT = "%d.%m.%y %H.%M.%S"


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

    def export(self, path=f"out/{dt.datetime.now().strftime(FORMAT)}.csv"):
        """
        Uses the **Export Data** button on the webpage to export the current leaderboard.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *./out/%d.%m.%y %H.%M.%S.csv*

        :param path: The path to save the exported data to
        """
        self._close_ad()
        path = path if os.path.splitext(path)[1] == ".csv" else f"{path}.csv"
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
