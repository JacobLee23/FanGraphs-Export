#! python3
# fangraphs/__init__.py

"""
Subpackage for scraping the FanGraphs **Leaders** pages.
"""

import os

import pandas as pd
from playwright.sync_api import sync_playwright

import fangraphs.exceptions


class __DecoratorAdapter:
    """
    Adapts a decorator for both function and method usage.
    """

    def __init__(self, decorator, func):
        self.decorator = decorator
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))


def __adapt(decorator):
    """
    Decorator for adapting decorators for function or method usage.
    """
    def wrapper(func):
        return __DecoratorAdapter(decorator, func)
    return wrapper


@__adapt
def fangraphs_scraper(func):

    def wrapper(scraper, /,  *, headless=True):
        with sync_playwright() as play:
            try:
                browser = play.chromium.launch(
                    headless=headless,
                )
                results = func(scraper(browser))
                return results
            finally:
                browser.close()

    return wrapper


class ScrapingUtilities:
    """
    Parent class inherited by all classes in ``fangraphs.*`` modules.
    """

    def __init__(self, browser, address: str, queries):
        """
        :param browser: A Playwright ``Browser`` object
        :param address: The URL to the FanGraphs leaderboard
        :param queries: A class (to initialize) containing all necessary CSS selectors
        :type queries: type
        """
        self.browser = browser
        self.page = self.browser.new_page(accept_downloads=True)
        self.address = address
        self.queries = queries(self.page)

        self.reset()

    def _close_ad(self):
        """
        Closes the ad which may interfere with clicking other page elements.
        """
        elem = self.page.query_selector(".ezmob-footer-close")
        if self.page.query_selector_all(
                "#ezmob-wrapper > div[style='display: none;']"
        ):
            return
        if elem:
            elem.click()

    def list_queries(self):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :rtype: list
        """
        return list(vars(self.queries))

    def list_options(self, query: str):
        """
        Lists the possible options which a filter query can be configured to.

        :param query: The filter query
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        sel_obj = vars(self.queries).get(query.lower())
        if sel_obj is None:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return sel_obj.list_options()

    def current_option(self, query: str):
        """
        Retrieves the option which a filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        sel_obj = vars(self.queries).get(query.lower())
        if sel_obj is None:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return sel_obj.current_option()

    def configure(self, query: str, option: str):
        """
        Configures a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        :raises FanGraphs.exceptions.InvalidFilterQuery: Invalid argument ``query``
        """
        self._close_ad()
        sel_obj = vars(self.queries).get(query.lower())
        if sel_obj is None:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        sel_obj.configure(option)

    def export(self):
        """
        Exports the data in the current leaderboard as a DataFrame.

        The **Export Data** button is clicked, downloading a CSV file containing the data.
        The CSV is read and the data is stored in a DataFrame.

        :return: The leaderboard data
        :rtype: pandas.DataFrame
        """
        self._close_ad()
        with self.page.expect_download() as down_info:
            self.page.click(self.queries.export_data)
        download = down_info.value
        download_path = download.path()
        dataframe = pd.read_csv(download_path)

        os.remove(download_path)
        return dataframe

    def reset(self):
        """
        Navigates :py:attr:`page` to :py:attr:`address`.
        """
        self.page.goto(self.address, timeout=0)
        if self.queries.waitfor:
            self.page.wait_for_selector(self.queries.waitfor)
