#! python3
# fangraphs/tests/test_depth_charts.py

"""
Unit tests for :py:mod:`fangraphs.depth_charts`.
"""

from urllib.request import urlopen


class TestDepthCharts:
    """
    :py:class:`fangraphs.depth_charts.DepthCharts`.
    """

    address = "https://fangraphs.com/depthcharts.aspx"

    def test_address(self):
        res = urlopen(self.address)
        assert res.getcode() == 200
