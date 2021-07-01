#! usr/bin/env python
# fangraphs/selectors/_depth_charts.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.depth_charts`.
"""

from typing import *

from . import widgets


class DepthCharts(widgets.Selectors):
    """
    Widget handling for :py:class:`fangraphs.teams.DepthCharts`.
    """
    _selections = {
        "table_type": {"root_selector": "#tsPosition"}
    }

    def __init__(self, page):
        super().__init__(page)


class Teams:
    """

    """
    __selector = "#menu-team > .menu-team"
    __opt_sels = [
        f"ul > a:nth-child({i})" for i in range(1, 6)
    ]

    @classmethod
    def compile_selectors(cls, obj) -> Generator[tuple[str, str], None, None]:
        """
        Compiles the full CSS selector for each of the items in the ``object`` class attribute.

        :param obj: An object
        :return: The attribute name and the full CSS selector for the attribute
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
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)

    class ALCentral:
        """
        CSS selectors for AL Central teams.
        """

        selector = ".menu-team-header:nth-child(2)"
        options = ["indians", "royals", "tigers", "twins", "white_sox"]

        def __init__(self):
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)

    class ALWest:
        """
        CSS selectors for AL West teams.
        """

        selector = ".menu-team-header:nth-child(3)"
        options = ["angels", "astros", "athletics", "mariners", "rangers"]

        def __init__(self):
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLEast:
        """
        CSS selectors for NL East teams.
        """

        selector = ".menu-team-header:nth-child(4)"
        options = ["braves", "marlins", "mets", "nationals", "phillies"]

        def __init__(self):
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLCentral:
        """
        CSS selectors for NL Central teams.
        """

        selector = ".menu-team-header:nth-child(5)"
        options = ["brewers", "cardinals", "cubs", "pirates", "reds"]

        def __init__(self):
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)

    class NLWest:
        """
        CSS selectors for NL West teams.
        """

        selector = ".menu-team-header:nth-child(6)"
        options = ["diamondbacks", "dodgers", "giants", "padres", "rockies"]

        def __init__(self):
            for key, selector in Teams.compile_selectors(self):
                self.__setattr__(key, selector)
