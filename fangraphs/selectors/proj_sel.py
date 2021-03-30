#! python3
# FanGraphs/selectors/proj_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.projections.projections`.
"""


class Projections:
    selections = {
        "stat": "#ProjectionBoard1_tsStats",
        "position": "#ProjectionBoard1_tsPosition",
        "projection": "#ProjectionBoard1_tsProj"
    }
    dropdowns = {
        "team": "#ProjectionBoard1_rcbTeam_Input",
        "league": "#ProjectionBoard1_rcbLeague_Input"
    }
    dropdown_options = {
        "team": "#ProjectionBoard1_rcbTeam_DropDown",
        "league": "#ProjectionBoard1_rcbLeague_DropDown"
    }
