#! python3
# fangraphs/selectors/dcharts_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.depth_charts`.
"""

from fangraphs import selectors


class DepthCharts:
    """
    CSS selectors for :py:class:`fangraphs.teams.DepthCharts`.
    """
    __selections_type_1 = {
        "view_type": "#tsPosition"
    }
    waitfor = ""
    export_data = ""

    def __init__(self, page):
        for key, val in self.__selections_type_1.items():
            self.__setattr__(key, selectors.SelectionsType1(page, val))
