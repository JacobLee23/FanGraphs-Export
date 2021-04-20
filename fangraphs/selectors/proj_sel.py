#! python3
# FanGraphs/selectors/proj_sel.py

from fangraphs import selectors

"""
CSS selectors for the classes in :py:mod:`fangraphs.projections`.
"""


class Projections:
    """
    CSS selectors for :py:class:`fangraphs.projections.Projections`.
    """
    __selections_type_1 = {
        "stat": "#ProjectionBoard1_tsStats",
        "position": "#ProjectionBoard1_tsPosition",
        "projection": "#ProjectionBoard1_tsProj",
        "update": "#ProjectionBoard1_tsUpdate"
    }
    __dropdowns_type_1 = {
        "team": ("#ProjectionBoard1_rcbTeam_Input", "#ProjectionBoard1_rcbTeam_DropDown"),
        "league": ("#ProjectionBoard1_rcbLeague_Input", "#ProjectionBoard1_rcbLeague_DropDown")
    }
    waitfor = ""
    export_data = "#ProjectionBoard1_cmdCSV"

    def __init__(self, page):
        for key, val in self.__selections_type_1.items():
            self.__setattr__(key, selectors.SelectionsType1(page, val))
        for key, val in self.__dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
