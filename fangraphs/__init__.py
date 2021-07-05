#! usr/bin/env python
# fangraphs/__init__.py

"""

"""

import os
import re
from typing import *

import bs4
import pandas as pd
from playwright.sync_api import sync_playwright

import fangraphs.exceptions
from fangraphs.selectors.widgets import WIDGET_TYPES


PID_REGEX = re.compile(r"playerid=(.*)")
PID_POS_REGEX = re.compile(r"playerid=(.*)&position=(.*)")


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

    def wrapper(scraper, *, headless=True):
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
        Exports the data_tables in the current leaderboard as a DataFrame.

        The **Export Data** button is clicked, downloading a CSV file containing the data_tables.
        The CSV is read and the data_tables is stored in a DataFrame.

        :return: The leaderboard data_tables
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


class FilterWidgets:
    """

    """
    _widget_class = None

    address: str = None

    class TableData(NamedTuple):
        dataframe: pd.DataFrame
        row_elems: bs4.ResultSet
        header_elems: bs4.ResultSet

    class Widget(NamedTuple):
        wname: str
        wtype: type

    def __init__(
            self, *,
            pre_clicks: tuple[str] = (),
            table_size: Optional[str] = None,
            menu_expansion: Optional[str] = None,
            quick_configure: Optional[str] = None,
            post_clicks: tuple[str] = (),
            **kwargs
    ):
        if self._widget_class is None:
            raise NotImplementedError
        if self.address is None:
            raise NotImplementedError

        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch()
        self.page = self.__browser.new_page(
            accept_downloads=True
        )
        self.page.goto(self.address, timeout=0)

        self.filter_widgets = self._widget_class(self.page)
        for css in pre_clicks:
            self.page.click(css)
        if table_size is not None:
            self.set_table_size(table_size)
        if menu_expansion is not None:
            self.expand_menu(menu_expansion)
        if quick_configure is not None:
            self.page.click(quick_configure)
        else:
            self.filter_widgets.configure(**kwargs)
        for css in post_clicks:
            self.page.click(css)

        self.soup = None

    def __del__(self):
        self.__browser.close()
        self.__play.stop()

    @property
    def soup(self) -> bs4.BeautifulSoup:
        """

        :return:
        """
        return self._soup

    @soup.setter
    def soup(self, value) -> None:
        """

        """
        html = self.page.content()
        self._soup = bs4.BeautifulSoup(html, features="lxml")

    @classmethod
    def widgets(cls) -> tuple:
        """

        :return:
        """
        widgets = []

        for wname, wtype in WIDGET_TYPES.items():
            if (d := cls._widget_class.__dict__.get(wname)) is not None:
                for name in d:
                    widgets.append(
                        cls.Widget(wname=name, wtype=wtype)
                    )

        return tuple(widgets)

    @classmethod
    def menu_expansions(cls) -> Optional[tuple[str]]:
        """

        :return:
        """
        try:
            expansions = tuple(cls._widget_class.menu_expansion_css)
            return expansions
        except AttributeError:
            return None

    def expand_menu(self, menu_expansion: str) -> None:
        """

        :param menu_expansion:
        """

        menu_expansion = menu_expansion.title()

        try:
            css = self._widget_class.menu_expansion_css.get(menu_expansion)
        except AttributeError as err:
            raise NotImplementedError from err

        if css is None:
            raise fangraphs.exceptions.InvalidFilterOption(menu_expansion)

        self.page.click(css)

    def set_table_size(self, table_size: str) -> None:
        """

        :param table_size:
        """
        try:
            root_elem = self.page.query_selector(self._widget_class.table_size_css)
            option_elems = root_elem.query_selector_all("option")
        except AttributeError as err:
            raise NotImplementedError from err

        options = [
            e.text_content() for e in option_elems
        ]
        if table_size.lower() not in (opts := [o.lower() for o in options]):
            raise fangraphs.exceptions.InvalidFilterOption(table_size)
        label = options[opts.index(table_size.lower())]
        root_elem.select_option(label=label)

    def scrape_table(
            self, table: bs4.Tag, css_h: str = "thead > tr",
            css_r: str = "tbody > tr"
    ) -> TableData:
        """

        :param table:
        :param css_h:
        :param css_r:
        :return:
        """
        header_elems = table.select_one(css_h).select("th")
        row_elems = table.select(css_r)

        dataframe = pd.DataFrame(
            data=[
                [e.text for e in r.select("td")]
                for r in row_elems
            ],
            columns=[e.text for e in header_elems]
        )

        table_data = self.TableData(dataframe, row_elems, header_elems)

        return table_data

    def _close_ad(self) -> None:
        """

        """
        if self.page.query_selector_all(
                "#ezmob-wrapper > div[style='display: none;']"
        ):
            return

        elem = self.page.query_selector(".ezmob-footer-close")
        if elem:
            elem.click()

    def export_data(self) -> pd.DataFrame:
        """

        :return:
        """
        try:
            css = self._widget_class.export_data_css
        except AttributeError as err:
            raise NotImplementedError from err

        self._close_ad()

        with self.page.expect_download() as down_info:
            self.page.click(css)

        download = down_info.value
        download_path = download.path()
        dataframe = pd.read_csv(download_path)

        os.remove(download_path)
        return dataframe
