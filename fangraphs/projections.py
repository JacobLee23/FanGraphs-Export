#! usr/bin/env python
# fangraphs/projections.py

"""
Scraper for the webpages under the FanGraphs **Projections** tab.
"""

import pandas as pd

from fangraphs import FilterWidgets
from fangraphs.selectors import projections_


class Projections(FilterWidgets):
    """
    Scraper for the FanGraphs `Projections`_ page.

    .. _Projections: https://fangraphs.com/projections.aspx
    """
    _widget_class = projections_.Projections
    address = "https://fangraphs.com/projections.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        """

        """
        dataframe = self.export_data()

        dataframe.drop(columns=["-1", "-1.1", "-1.2", "-1.3"], inplace=True)

        self._data = dataframe
