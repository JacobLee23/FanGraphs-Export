#! python3
# fangraphs/teams.py

"""
Scrapers for the webpages under the FanGraphs **Teams** tab.
"""

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import teams_sel


class Teams:
    """
    Scrapes the FanGraphs `Teams`_ pages.

    .. _Teams: https://fangraphs.com/teams
    """
