#! python3
# fangraphs/selectors/proj_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.projections`.
"""

from fangraphs import selectors


class Projections(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.projections.Projections`.
    """
    _selections = {
        "stat": {"css_selector": "#ProjectionBoard1_tsStats"},
        "position": {"css_selector": "#ProjectionBoard1_tsPosition"},
        "projection": {"css_selector": "#ProjectionBoard1_tsProj"},
        "update": {"css_selector": "#ProjectionBoard1_tsUpdate"}
    }
    __dropdowns_type_1 = {
        "team": ("#ProjectionBoard1_rcbTeam_Input", "#ProjectionBoard1_rcbTeam_DropDown"),
        "league": ("#ProjectionBoard1_rcbLeague_Input", "#ProjectionBoard1_rcbLeague_DropDown")
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
