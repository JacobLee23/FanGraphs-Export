#! python3
# FanGraphs/projections/__init__.py

"""
Scraper for the webpages under the FanGraphs **Projections** tab.
"""

from fangraphs import ScrapingUtilities
from fangraphs.selectors import proj_sel


class Projections(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Projections`_ page.

    .. _Projections: https://fangraphs.com/projections.aspx
    """

    address = "https://fangraphs.com/projections.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, proj_sel.Projections)
        self.queries = proj_sel.Projections(self.page)
