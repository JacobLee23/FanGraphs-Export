#! python3
# fangraphs/tests/test_teams.py

"""
Unit tests for :py:mod:`fangraphs.teams`.
"""

from urllib.request import urlopen


class TestDepthCharts:
    """
    :py:class:`fangraphs.teams.DepthCharts`.
    """

    address = "https://fangraphs.com/depthcharts.aspx"

    def test_address(self):
        res = urlopen(self.address)
        assert res.getcode() == 200
