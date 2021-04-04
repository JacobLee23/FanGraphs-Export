#! python3
# fangraphs/selectors/dcharts_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.teams`.
"""


class DepthCharts:
    """
    CSS selectors for :py:class:`fangraphs.teams.DepthCharts`.
    """
    selections = {
        "type": "#tsPosition"
    }
    dropdowns = {
        "al_east": ".menu-team > .menu-team-header:nth-child(1)",
        "al_central": ".menu-team > .menu-team-header:nth-child(2)",
        "al_west": ".menu-team > .menu-team-header:nth-child(3)",
        "nl_east": ".menu-team > .menu-team-header:nth-child(4)",
        "nl_central": ".menu-team > .menu-team-header:nth-child(5)",
        "nl_west": ".menu-team > .menu-team-header:nth-child(6)",
        "free_agents": ".menu-team > .menu-team-header:nth-child(7)",
    }
    waitfor = ""
    export_data = ""


class Teams:
    """
    CSS selectors for :py:class:`fangraphs.teams.Teams`.
    """
    selections = {
        "type": ".team-nav-bar"
    }
    dropdowns = {
        "team": ".select-change-team",
        "pos_stat": ".pos-stat",
        "pit_stat": ".pit-stat"
    }
