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
    """
    CSS selectors for :py:class:`fangraphs.teams.Team`.
    """
    __selector = "#menu-team > .menu-team"
    __opt_sels = [
        f"ul > a:nth-child({i})" for i in range(1, 6)
    ]

    @classmethod
    def compile_selectors(cls, obj):
        """
        Compiles the full CSS selector for each of the items in the ``object`` class attribute.

        :param obj: An object
        :return: The name and the full CSS selector for each attribute
        :rtype: tuple[str, str]
        """
        for key, val in zip(obj.options, cls.__opt_sels):
            selector = f"{cls.__selector} > {obj.selector} > {val}"
            yield key, selector

    class ALEast:
        """
        CSS selectors for AL East teams.
        """

        selector = ".menu-team-header:nth-child(1)"
        options = ["blue_jays", "orioles", "rays", "red_sox", "yankees"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)

    class ALCentral:
        """
        CSS selectors for AL Central teams.
        """

        selector = ".menu-team-header:nth-child(2)"
        options = ["indians", "royals", "tigers", "twins", "white_sox"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)

    class ALWest:
        """
        CSS selectors for AL West teams.
        """

        selector = ".menu-team-header:nth-child(3)"
        options = ["angels", "astros", "athletics", "mariners", "rangers"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLEast:
        """
        CSS selectors for NL East teams.
        """

        selector = ".menu-team-header:nth-child(4)"
        options = ["braves", "marlins", "mets", "nationals", "phillies"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLCentral:
        """
        CSS selectors for NL Central teams.
        """

        selector = ".menu-team-header:nth-child(5)"
        options = ["brewers", "cardinals", "cubs", "pirates", "reds"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLWest:
        """
        CSS selectors for NL West teams.
        """

        selector = ".menu-team-header:nth-child(6)"
        options = ["diamondbacks", "dodgers", "giants", "padres", "rockies"]

        def __init__(self):
            for key, selector in Team.compile_selectors(self):
                self.__setattr__(key, selector)
