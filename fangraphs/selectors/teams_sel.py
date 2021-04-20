#! python3
# fangraphs/selectors/dcharts_sel.py

from fangraphs import selectors

"""
CSS selectors for the classes in :py:mod:`fangraphs.teams`.
"""


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


class Team:
    __selector = "#menu-team > .menu-team"
    __opt_sels = [
        f"ul > a:nth-child({i})" for i in range(1, 6)
    ]

    @classmethod
    def compile(cls, obj):
        for key, val in zip(obj.options, cls.__opt_sels):
            selector = f"{cls.__selector} > {obj.selector} > {val}"
            yield key, selector

    class ALEast:
        selector = ".menu-team-header:nth-child(1)"
        options = ["blue_jays", "orioles", "rays", "red_sox", "yankees"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)

    class ALCentral:
        selector = ".menu-team-header:nth-child(2)"
        options = ["indians", "royals", "tigers", "twins", "white_sox"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)

    class ALWest:
        selector = ".menu-team-header:nth-child(3)"
        options = ["angels", "astros", "athletics", "mariners", "rangers"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)

    class NLEast:
        selector = ".menu-team-header:nth-child(4)"
        options = ["braves", "marlins", "mets", "nationals", "phillies"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)

    class NLCentral:
        selector = ".menu-team-header:nth-child(5)"
        options = ["brewers", "cardinals", "cubs", "pirates", "reds"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)

    class NLWest:
        selector = ".menu-team-header:nth-child(6)"
        options = ["diamondbacks", "dodgers", "giants", "padres", "rockies"]

        def __init__(self):
            for key, selector in Team.compile(self):
                self.__setattr__(key, selector)
