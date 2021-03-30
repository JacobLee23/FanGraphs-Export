#! python3
# FanGraphs/projections/projections.py

"""
Scraper for the webpages under the FanGraphs **Projections** tab.
"""

import fangraphs.exceptions
from fangraphs import ScrapingUtilities
from fangraphs import selectors
from fangraphs.selectors import proj_sel


class Projections(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Projections`_ page.

    .. _Projections: https://fangraphs.com/projections.aspx
    """
    __selections = {}
    __dropdowns = {}

    address = "https://fangraphs.com/projections.aspx"

    def __init__(self):
        super().__init__(self.address)

    def __enter__(self):
        self._browser_init()
        self.reset()
        self.__compile_selectors()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.quit()

    def __compile_selectors(self):
        for cat, sel in proj_sel.Projections.selections.items():
            self.__selections.setdefault(
                cat, selectors.Selections(self.soup, sel, "> div > ul > li")
            )
        for cat, sel in proj_sel.Projections.dropdowns.items():
            options = proj_sel.Projections.dropdown_options[cat]
            self.__dropdowns.setdefault(
                cat, selectors.Dropdowns(self.soup, sel, "> div > ul > li", options)
            )
