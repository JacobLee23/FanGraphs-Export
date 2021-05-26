#! python3
# fangraphs/scores.py

"""
Scrapers for the webpages under the FanGraphs **Scores** tab.
"""

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import scores_sel


class Live(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Live Scoreboard`_ page.

    .. _Live Scoreboard: https://www.fangraphs.com/livescoreboard.aspx
    """

    address = "https://www.fangraphs.com/livescoreboard.aspx"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.Live)
