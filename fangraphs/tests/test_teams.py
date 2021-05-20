#! python3
# fangraphs/tests/test_teams.py

"""
Unit tests for :py:mod:`fangraphs.teams`.
"""

from urllib.request import urlopen


class TestSummary:
    """
    :py:class:`fangraphs.teams.Teams`.
    """

    address = "https://fangraphs.com/teams/angels"

    def test_address(self):
        res = urlopen(self.address)
        assert res.getcode() == 200
