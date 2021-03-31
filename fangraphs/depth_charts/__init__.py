#! python3
# fangraphs/depth_charts/__init__.py

import fangraphs.exceptions
from fangraphs import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import dcharts_sel


class DepthCharts(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Depth Charts`_ page.

    .. _Depth Charts: https://fangraphs.com/depthcharts.aspx
    """
    __selections = {}

    address = "https://fangraphs.com/depthcharts.aspx"

    def __init__(self):
        super().__init__(
            self.address, selector_mod=dcharts_sel.DepthCharts
        )
        self.__enter__()

    def __enter__(self):
        self._browser_init()
        self.reset()
        self.__compile_selectors()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.quit()

    def __compile_selectors(self):
        for cat, sel in dcharts_sel.DepthCharts.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> div > ul > li")
            )

    @classmethod
    def list_queries(cls):
        queries = []
        queries.extend(list(cls.__selections))
        return queries

    def list_options(self, query: str):
        query = query.lower()
        if query in self.__selections:
            options = self.__selections[query].list_options()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return options

    def current_option(self, query: str):
        query = query.lower()
        if query in self.__selections:
            option = self.__selections[query].current_option()
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
        return option

    def configure(self, query: str, option: str):
        query = query.lower()
        if query in self.__selections:
            self.__selections[query].configure(self.page, option)
        else:
            raise fangraphs.exceptions.InvalidFilterQuery(query)
