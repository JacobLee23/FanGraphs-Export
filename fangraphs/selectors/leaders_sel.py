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
            "css_selectors": [
                f".controls-stats > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "table_type": {
            "css_selectors": [
                f".controls-board-view > .fgButton:nth-child({n})"
                for n in range(1, 4)
            ]
        }
    }
    dropdowns_type_2 = {
        "minimum": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
        "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
        "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
        "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
        "determine": ".controls-stats.stat-determined > div:nth-child(1) > .fg-selection-box__selection"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_2.items():
            self.__setattr__(key, selectors.DropdownsType2(page, val))


class International(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.International`.
    """
    selections_type_2 = {
        "stat": {
            "css_selectors": [
                f".controls-stats > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "view_type": {
            "css_selectors": [
                f".controls-board-view > .fgButton:nth-child({n})"
                for n in range(1, 3)
            ]
        }
    }
    dropdowns_type_2 = {
        "position": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
        "minimum": ".controls-stats:nth-child(1) > div:nth-child(4) > .fg-selection-box__selection",
        "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
        "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
        "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
        "league": ".controls-stats:nth-child(3) > div:nth-child(1) > .fg-selection-box__selection",
        "team": ".controls-stats:nth-child(3) > div:nth-child(2) > .fg-selection-box__selection",
    }
    __checkboxes = {
        "split_seasons": ".controls-stats > label.fg-checkbox"
    }
    waitfor = ".fg-data-grid.table-type"
    export_data = ".data-export"

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_2.items():
            self.__setattr__(key, selectors.DropdownsType2(page, val))
        for key, val in self.__checkboxes.items():
            self.__setattr__(key, selectors.Checkboxes(page, val))


class MajorLeague(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.MajorLeague`.
    """
    _selections = {
        "group": {"css_selector": "#LeaderBoard1_tsGroup"},
        "stat": {"css_selector": "#LeaderBoard1_tsStats"},
        "position": {"css_selector": "#LeaderBoard1_tsPosition"},
        "table_type": {"css_selector": "#LeaderBoard1_tsType"}
    }
    dropdowns_type_1 = {
        "league": ('#LeaderBoard1_rcbAge1_Input', '#LeaderBoard1_rcbAge1_DropDown'),
        "team": ('#LeaderBoard1_rcbTeam_Input', '#LeaderBoard1_rcbTeam_DropDown'),
        "single_season": ('#LeaderBoard1_rcbSeason_Input', '#LeaderBoard1_rcbSeason_DropDown'),
        "split": ('#LeaderBoard1_rcbMonth_Input', '#LeaderBoard1_rcbMonth_DropDown'),
        "minimum": ('#LeaderBoard1_rcbMin_Input', '#LeaderBoard1_rcbMin_DropDown'),
        "season1": ('#LeaderBoard1_rcbSeason1_Input', '#LeaderBoard1_rcbSeason1_DropDown'),
        "season2": ('#LeaderBoard1_rcbSeason2_Input', '#LeaderBoard1_rcbSeason2_DropDown'),
        "age1": ('#LeaderBoard1_rcbAge1_Input', '#LeaderBoard1_rcbAge1_DropDown'),
        "age2": ('#LeaderBoard1_rcbAge2_Input', '#LeaderBoard1_rcbAge2_DropDown')
    }
    checkboxes = {
        "split_teams": "#LeaderBoard1_cbTeams",
        "active_roster": "#LeaderBoard1_cbActive",
        "hof": "#LeaderBoard1_cbHOF",
        "split_seasons": "#LeaderBoard1_cbSeason",
        "rookies": "#LeaderBoard1_cbRookie"
    }
    buttons = {
        "season1": "#LeaderBoard1_btnMSeason",
        "season2": "#LeaderBoard1_btnMSeason",
        "age1": "#LeaderBoard1_cmdAge",
        "age2": "#LeaderBoard1_cmdAge"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
        for key, val in self.checkboxes.items():
            self.__setattr__(key, selectors.Checkboxes(page, val))


class SeasonStat(selectors.Selectors):
    """
    CSS selectors for :py:class:`fangraphs.leaders.SeasonStat`.
    """
    _selections = {
        "stat": {
            "css_selectors": [
                f"div[class*='fgButton button-green']:nth-child({n})"
                for n in range(1, 3)
            ]
        },
        "table_type": {
            "css_selectors": [
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
            "css_selectors": [
                f".fgBin.row-button > div[class*='button-green fgButton']:nth-child({n})"
                for n in range(1, 5)
            ]
        },
        "stat": {
            "css_selectors": [
                f".fgBin.row-button > div[class*='button-green fgButton']:nth-child({n})"
                for n in range(6, 8)
            ]
        },
        "table_type": {
            "css_selectors": [
                f"#root-button-stats > div:nth-child({n})"
                for n in range(1, 4)
            ]
        }
    }
    dropdowns_type_3 = {
        "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
        "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
        "groupby": ".fg-dropdown.group-by",
        "handedness": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "home_away": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(2)",
        "batted_ball": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(3)",
        "situation": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(4)",
        "count": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(5)",
        "batting_order": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "position": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(2)",
        "inning": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(3)",
        "leverage": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(4)",
        "shifts": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(5)",
        "team": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(1)",
        "opponent": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(2)"
    }
    switches = {
        "split_teams": "#stack-buttons > div:nth-child(2)",
        "auto_pt": "#stack-buttons > div:nth-child(3)"
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_3.items():
            self.__setattr__(key, selectors.DropdownsType3(page, val))
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
    dropdowns_type_1 = {
        "season": ("#WARBoard1_rcbSeason_Input", "#WARBoard1_rcbSeason_DropDown"),
        "team": ("#WARBoard1_rcbTeam_Input", "#WARBoard1_rcbTeam_DropDown"),
        "view_type": ("#WARBoard1_rcbType_Input", "#WARBoard1_rcbType_DropDown")
    }

    def __init__(self, page):
        super().__init__(page)
        for key, val in self.dropdowns_type_1.items():
            self.__setattr__(key, selectors.DropdownsType1(page, *val))
