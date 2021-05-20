#! python3
# fangraphs/tests/test_projections.py

"""
Unit tests for :py:mod:`fangraphs.projections`.
"""

from urllib.request import urlopen


class TestProjections:
    """
    :py:class:`fangraphs.projections.Projections`
    """

    address = "https://fangraphs.com/projections.aspx"

    def test_address(self):
        """
        :py:meth:`fangraphs.projections.Projections.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200
