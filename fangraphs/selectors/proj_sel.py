#! python3
# FanGraphs/selectors/proj_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.projections`.
"""


class Projections:
    """
    CSS selectors for :py:class:`fangraphs.projections.Projections`.
    """
    selections = {
        "stat": "#ProjectionBoard1_tsStats",
        "position": "#ProjectionBoard1_tsPosition",
        "projection": "#ProjectionBoard1_tsProj",
        "update": "#ProjectionBoard1_tsUpdate"
    }
    dropdowns = {
        "team": "#ProjectionBoard1_rcbTeam_Input",
        "league": "#ProjectionBoard1_rcbLeague_Input",
    }
    dropdown_options = {
        "team": "#ProjectionBoard1_rcbTeam_DropDown",
        "league": "#ProjectionBoard1_rcbLeague_DropDown"
    }
    waitfor = ""
    export_data = "#ProjectionBoard1_cmdCSV"
