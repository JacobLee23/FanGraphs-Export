#! usr/bin/env python
# fangraphs/selectors/_projections.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.projections`.
"""

from . import widgets


class Projections(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.projections.Projections`.
    """
    _selections = {
        "stat": {"root_selector": "#ProjectionBoard1_tsStats"},
        "position": {"root_selector": "#ProjectionBoard1_tsPosition"},
        "projection": {"root_selector": "#ProjectionBoard1_tsProj"},
        "update": {"root_selector": "#ProjectionBoard1_tsUpdate"}
    }
    _dropdowns = {
        "team": {
            "root_selector": "#ProjectionBoard1_rcbTeam_Input",
            "dropdown_selector": "#ProjectionBoard1_rcbTeam_DropDown"
        },
        "league": {
            "root_selector": "#ProjectionBoard1_rcbLeague_Input",
            "dropdown_selector": "#ProjectionBoard1_rcbLeague_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)
