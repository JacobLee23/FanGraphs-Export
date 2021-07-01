#! python3
# fangraphs/selectors/leaders_sel.py

from fangraphs import selectors

"""
CSS selectors for the classes in :py:mod:`fangraphs.leaders`.
"""


class GameSpan(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.GameSpan`.
    """
    _selections = {
        "stat": {
            "root_selectors": [
                f".controls-stats > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "table_type": {
            "root_selectors": [
                f".controls-board-view > .fgButton:nth-child({n})"
                for n in range(1, 4)
            ]
        }
    }
    _dropdowns = {
        "minimum": {
            "root_selector": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection"
        },
        "single_season": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection"
        },
        "season1": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection"
        },
        "season2": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection"
        },
        "determine": {
            "root_selector": ".controls-stats.stat-determined > div:nth-child(1) > .fg-selection-box__selection"
        }
    }

    def __init__(self, page):
        super().__init__(page)


class International(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.International`.
    """
    _selections = {
        "stat": {
            "root_selectors": [
                f".controls-stats > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "view_type": {
            "root_selectors": [
                f".controls-board-view > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        }
    }
    _dropdowns = {
        "position": {
            "root_selector": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection"
        },
        "minimum": {
            "root_selector": ".controls-stats:nth-child(1) > div:nth-child(4) > .fg-selection-box__selection"
        },
        "single_season": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection"
        },
        "season1": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection"
        },
        "season2": {
            "root_selector": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection"
        },
        "league": {
            "root_selector": ".controls-stats:nth-child(3) > div:nth-child(1) > .fg-selection-box__selection"
        },
        "team": {
            "root_selector": ".controls-stats:nth-child(3) > div:nth-child(2) > .fg-selection-box__selection"
        }
    }
    __checkboxes = {
        "split_seasons": ".controls-stats > label.fg-checkbox"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.__checkboxes.items():
            self.__setattr__(key, selectors.Checkboxes(page, val))


class MajorLeague(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.MajorLeague`.
    """
    _selections = {
        "group": {"root_selector": "#LeaderBoard1_tsGroup"},
        "stat": {"root_selector": "#LeaderBoard1_tsStats"},
        "position": {"root_selector": "#LeaderBoard1_tsPosition"},
        "table_type": {"root_selector": "#LeaderBoard1_tsType"}
    }
    _dropdowns = {
        "league": {
            "root_selector": "#LeaderBoard1_rcbAge1_Input",
            "dropdown_selector": "#LeaderBoard1_rcbAge1_DropDown",
        },
        "team": {
            "root_selector": "#LeaderBoard1_rcbTeam_Input",
            "dropdown_selector": "#LeaderBoard1_rcbTeam_DropDown"
        },
        "single_season": {
            "root_selector": "#LeaderBoard1_rcbSeason_Input",
            "dropdown_selector": "#LeaderBoard1_rcbSeason_DropDow"
        },
        "split": {
            "root_selector": "#LeaderBoard1_rcbMonth_Input",
            "dropdown_selector": "#LeaderBoard1_rcbMonth_DropDow"
        },
        "minimum": {
            "root_selector": "#LeaderBoard1_rcbMin_Input",
            "dropdown_selector": "#LeaderBoard1_rcbMin_DropDown"
        },
        "season1": {
            "root_selector": "#LeaderBoard1_rcbSeason1_Input",
            "dropdown_selector": "#LeaderBoard1_rcbSeason1_DropDown",
            "button_selector": "#LeaderBoard1_btnMSeason"
        },
        "season2": {
            "root_selector": "#LeaderBoard1_rcbSeason2_Input",
            "dropdown_selector": "#LeaderBoard1_rcbSeason2_DropDown",
            "button_selector": "#LeaderBoard1_btnMSeason"
        },
        "age1": {
            "root_selector": "#LeaderBoard1_rcbAge1_Input",
            "dropdown_selector": "#LeaderBoard1_rcbAge1_DropDown",
            "button_selector": "#LeaderBoard1_cmdAge"
        },
        "age2": {
            "root_selector": "#LeaderBoard1_rcbAge2_Input",
            "dropdown_selector": "#LeaderBoard1_rcbAge2_DropDow",
            "button_selector": "#LeaderBoard1_cmdAge"
        }
    }
    checkboxes = {
        "split_teams": "#LeaderBoard1_cbTeams",
        "active_roster": "#LeaderBoard1_cbActive",
        "hof": "#LeaderBoard1_cbHOF",
        "split_seasons": "#LeaderBoard1_cbSeason",
        "rookies": "#LeaderBoard1_cbRookie"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.checkboxes.items():
            self.__setattr__(key, selectors.Checkboxes(page, val))


class SeasonStat(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.SeasonStat`.
    """
    _selections = {
        "stat": {
            "root_selectors": [
                f"div[class*='fgButton button-green']:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "table_type": {
            "root_selectors": [
                f"div[class*='fgButton button-green']:nth-child({n})"
                for n in range(4, 7)
            ]
        }
    }
    dropdowns_type_3 = {
        "start_season": ".row-season > div:nth-child(2)",
        "end_season": ".row-season > div:nth-child(4)",
        "popular": ".season-grid-controls-dropdown-row-stats > div:nth-child(1)",
        "standard": ".season-grid-controls-dropdown-row-stats > div:nth-child(2)",
        "advanced": ".season-grid-controls-dropdown-row-stats > div:nth-child(3)",
        "statcast": ".season-grid-controls-dropdown-row-stats > div:nth-child(4)",
        "batted_ball": ".season-grid-controls-dropdown-row-stats > div:nth-child(5)",
        "win_probability": ".season-grid-controls-dropdown-row-stats > div:nth-child(6)",
        "pitch_type": ".season-grid-controls-dropdown-row-stats > div:nth-child(7)",
        "plate_discipline": ".season-grid-controls-dropdown-row-stats > div:nth-child(8)",
        "value": ".season-grid-controls-dropdown-row-stats > div:nth-child(9)"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_3.items():
            self.__setattr__(key, selectors.DropdownsType3(page, val))


class Splits(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.Splits`.
    """
    _selections = {
        "group": {
            "root_selectors": [
                f".fgBin.row-button > div[class*='button-green fgButton']:nth-child({n})"
                for n in range(1, 5)
            ]
        },
        "stat": {
            "root_selectors": [
                f".fgBin.row-button > div[class*='button-green fgButton']:nth-child({n})"
                for n in range(6, 8)
            ]
        },
        "table_type": {
            "root_selectors": [
                f"#root-button-stats > div:nth-child({n})"
                for n in range(1, 4)
            ]
        }
    }
    _dropdowns = {
        "time_filter": {
            "root_selector": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice"
        },
        "preset_range": {
            "root_selector": "#root-menu-time-filter > .fg-dropdown.splits.single-choice"
        },
        "group_by": {
            "root_selector": ".fg-dropdown.group-by"
        },
        "handedness": {
            "root_selector": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(1)"
        },
        "home_away": {
            "root_selector": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(2)"
        },
        "batted_ball": {
            "root_selector": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(3)"
        },
        "situation": {
            "root_selector": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(4)"
        },
        "count": {
            "root_selector": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(5)"
        },
        "batting_order": {
            "root_selector": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(1)"
        },
        "position": {
            "root_selector": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(2)"
        },
        "inning": {
            "root_selector": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(3)"
        },
        "leverage": {
            "root_selector": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(4)"
        },
        "shifts": {
            "root_selector": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(5)"
        },
        "team": {
            "root_selector": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(1)"
        },
        "opponent": {
            "root_selector": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(2)"
        }
    }
    switches = {
        "split_teams": "#stack-buttons > div:nth-child(2)",
        "auto_pt": "#stack-buttons > div:nth-child(3)"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.switches.items():
            self.__setattr__(key, selectors.Switches(page, val))


class QuickSplits:
    """
    CSS selectors for the quick splits available on the Splits leaderboard.
    """
    selector = ".quick-splits"

    @classmethod
    def compile(cls, obj):
        """
        Compiles the full CSS selector for each of the items in the ``object`` class attribute.

        :param obj: An object
        :return: The name and the full CSS selector for each attribute
        :rtype: tuple[str, str]
        """
        for key, val in obj.options.items():
            selector = f"{cls.selector} > {obj.selector} > {val}"
            yield key, selector

    class Batting:
        """
        CSS selectors for batting-related quick splits.
        """

        selector = "div:nth-child(1)"
        options = {
            "home": "div:nth-child(2) > .fgButton:nth-child(1)",
            "away": "div:nth-child(2) > .fgButton:nth-child(2)",
            "vs_lhp": "div:nth-child(3) > .fgButton:nth-child(1)",
            "vs_lhp_home": "div:nth-child(3) > .fgButton:nth-child(2)",
            "vs_lhp_away": "div:nth-child(3) > .fgButton:nth-child(3)",
            "vs_lhp_as_lhh": "div:nth-child(3) > .fgButton:nth-child(4)",
            "vs_lhp_as_rhh": ".div:nth-child(3) > .fgButton:nth-child(5)",
            "vs_rhp": "div:nth-child(4) > .fgButton:nth-child(1)",
            "vs_rhp_home": "div:nth-child(4) > .fgButton:nth-child(2)",
            "vs_rhp_away": "div:nth-child(4) > .fgButton:nth-child(3)",
            "vs_rhp_as_lhh": "div:nth-child(4) > .fgButton:nth-child(4)",
            "vs_rhp_as_rhh": "div:nth-child(4) > .fgButton:nth-child(5)",
        }

        def __init__(self):
            for key, selector in QuickSplits.compile(self):
                self.__setattr__(key, selector)

    class Pitching:
        """
        CSS selectors for pitching-related quick splits.
        """

        selector = "div:nth-child(1)"
        options = {
            "as_sp": "div:nth-child(1) .fgButton:nth-child(1)",
            "as_rp": "div:nth-child(1) .fgButton:nth-child(2)",
            "home": "div:nth-child(2) > .fgButton:nth-child(1)",
            "away": "div:nth-child(2) > .fgButton:nth-child(2)",
            "vs_lhh": "div:nth-child(3) > .fgButton:nth-child(1)",
            "vs_lhh_home": "div:nth-child(3) > .fgButton:nth-child(2)",
            "vs_lhh_away": "div:nth-child(3) > .fgButton:nth-child(3)",
            "vs_lhh_as_rhp": "div:nth-child(3) > .fgButton:nth-child(4)",
            "vs_lhh_as_lhp": "div:nth-child(3) > .fgButton:nth-child(5)",
            "vs_rhh": "div:nth-child(4) > .fgButton:nth-child(1)",
            "vs_rhh_home": ".div:nth-child(4) > .fgButton:nth-child(1)",
            "vs_rhh_away": "div:nth-child(4) > .fgButton:nth-child(1)",
            "vs_rhh_as_rhp": "div:nth-child(4) > .fgButton:nth-child(1)",
            "vs_rhh_as_lhp": "div:nth-child(4) > .fgButton:nth-child(1)"
        }

        def __init__(self):
            for key, selector in QuickSplits.compile(self):
                self.__setattr__(key, selector)


class WAR(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.WAR`.
    """
    _dropdowns = {
        "season": {
            "root_selector": "#WARBoard1_rcbSeason_Input",
            "dropdown_selector": "#WARBoard1_rcbSeason_Input"
        },
        "team": {
            "root_selector": "#WARBoard1_rcbTeam_Input",
            "dropdown_selector": "#WARBoard1_rcbTeam_DropDown"
        },
        "table_type": {
            "root_selector": "#WARBoard1_rcbType_Input",
            "dropdown_selector": "#WARBoard1_rcbType_DropDown"
        }
    }

    def __init__(self, page):
        super().__init__(page)
