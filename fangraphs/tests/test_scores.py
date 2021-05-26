#! python3
# fangraphs/tests/test_scores.py

"""
Unit tests for :py:mod:`fangraphs.scores`.
"""

from playwright.sync_api import sync_playwright
import pytest

from fangraphs.tests import BaseTests


class TestLive(BaseTests):
    """
    :py:class:`fangraphs.scores.Live`
    """
    address = "https://www.fangraphs.com/livescoreboard.aspx"
