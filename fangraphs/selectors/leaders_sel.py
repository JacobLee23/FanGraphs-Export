#! python3
# FanGraphs/selectors/leaders_sel.py

"""
CSS selectors for the classes in :py:mod:`fangraphs.leaders.leaders`.
"""


class GameSpan:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.GameSpan`.
    """
    selections = {
        "stat": [
            ".controls-stats > .fgButton:nth-child(1)",
            ".controls-stats > .fgButton:nth-child(2)"
        ],
        "type": [
            ".controls-board-view > .fgButton:nth-child(1)",
            ".controls-board-view > .fgButton:nth-child(2)",
            ".controls-board-view > .fgButton:nth-child(3)"
        ]
    }
    dropdowns = {
        "min_pa": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
        "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
        "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
        "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
        "determine": ".controls-stats.stat-determined > div:nth-child(1) > .fg-selection-box__selection"
    }
    waitfor = ".fg-data-grid.table-type"


class International:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.International`.
    """
    selections = {
        "stat": [
            ".controls-stats > .fgButton:nth-child(1)",
            ".controls-stats > .fgButton:nth-child(2)"
        ],
        "type": [
            ".controls-board-view > .fgButton:nth-child(1)",
            ".controls-board-view > .fgButton:nth-child(2)"
        ]
    }
    dropdowns = {
        "position": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
        "min": ".controls-stats:nth-child(1) > div:nth-child(4) > .fg-selection-box__selection",
        "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
        "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
        "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
        "league": ".controls-stats:nth-child(3) > div:nth-child(1) > .fg-selection-box__selection",
        "team": ".controls-stats:nth-child(3) > div:nth-child(2) > .fg-selection-box__selection",
    }
    switches = {
        "split_seasons": ".controls-stats > .fg-checkbox"
    }
    waitfor = ".fg-data-grid.table-type"


class MajorLeague:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.MajorLeague`.
    """
    selections = {
        "group": "#LeaderBoard1_tsGroup",
        "stat": "#LeaderBoard1_tsStats",
        "position": "#LeaderBoard1_tsPosition",
        "type": "#LeaderBoard1_tsType"
    }
    dropdowns = {
        "league": "#LeaderBoard1_rcbLeague_Input",
        "team": "#LeaderBoard1_rcbTeam_Input",
        "single_season": "#LeaderBoard1_rcbSeason_Input",
        "split": "#LeaderBoard1_rcbMonth_Input",
        "min_pa": "#LeaderBoard1_rcbMin_Input",
        "season1": "#LeaderBoard1_rcbSeason1_Input",
        "season2": "#LeaderBoard1_rcbSeason2_Input",
        "age1": "#LeaderBoard1_rcbAge1_Input",
        "age2": "#LeaderBoard1_rcbAge2_Input"
    }
    dropdown_options = {
        "league": "#LeaderBoard1_rcbLeague_DropDown",
        "team": "#LeaderBoard1_rcbTeam_DropDown",
        "single_season": "#LeaderBoard1_rcbSeason_DropDown",
        "split": "#LeaderBoard1_rcbMonth_DropDown",
        "min_pa": "#LeaderBoard1_rcbMin_DropDown",
        "season1": "#LeaderBoard1_rcbSeason1_DropDown",
        "season2": "#LeaderBoard1_rcbSeason2_DropDown",
        "age1": "#LeaderBoard1_rcbAge1_DropDown",
        "age2": "#LeaderBoard1_rcbAge2_DropDown"
    }
    switches = {
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


class SeasonStat:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.SeasonStat`.
    """
    selections = {
        "stat": [
            "div[class*='fgButton button-green']:nth-child(1)",
            "div[class*='fgButton button-green']:nth-child(2)"
        ],
        "type": [
            "div[class*='fgButton button-green']:nth-child(4)",
            "div[class*='fgButton button-green']:nth-child(5)",
            "div[class*='fgButton button-green']:nth-child(6)"
        ]
    }
    dropdowns = {
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
    waitfor = ".fg-data-grid.undefined"


class Splits:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.Splits`.
    """
    selections = {
        "group": [
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(1)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(2)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(3)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(4)"
        ],
        "stat": [
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(6)",
            ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(7)"
        ],
        "type": [
            "#root-buttons-stats > div:nth-child(1)",
            "#root-buttons-stats > div:nth-child(2)",
            "#root-buttons-stats > div:nth-child(3)"
        ]
    }
    dropdowns = {
        "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
        "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
        "groupby": ".fg-dropdown.group-by"
    }
    splits = {
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
        "opponent": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(2)",
    }
    quick_splits = {
        "batting_home": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(1)",
        "batting_away": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(2)",
        "vs_lhp": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(1)",
        "vs_lhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(2)",
        "vs_lhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(3)",
        "vs_lhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(4)",
        "vs_lhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(5)",
        "vs_rhp": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(2)",
        "vs_rhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(3)",
        "vs_rhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(4)",
        "vs_rhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(5)",
        "pitching_as_sp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(1)",
        "pitching_as_rp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(2)",
        "pitching_home": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(1)",
        "pitching_away": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(2)",
        "vs_lhh": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(1)",
        "vs_lhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(2)",
        "vs_lhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(3)",
        "vs_lhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(4)",
        "vs_lhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(5)",
        "vs_rhh": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
        "vs_rhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)"
    }
    switches = {
        "split_teams": "#stack-buttons > div:nth-child(2)",
        "auto_pt": "#stack-buttons > div:nth-child(3)"
    }
    waitfor = ".fg-data-grid.undefined"


class WAR:
    """
    CSS selectors for :py:class:`fangraphs.leaders.leaders.WAR`.
    """
    dropdowns = {
        "season": "#WARBoard1_rcbSeason_Input",
        "team": "#WARBoard1_rcbTeam_Input",
        "type": "#WARBoard1_rcbType_Input"
    }
    dropdown_options = {
        "season": "#WARBoard1_rcbSeason_DropDown",
        "team": "#WARBoard1_rcbTeam_DropDown",
        "type": "#WARBoard1_rcbType_DropDown"
    }
    waitfor = ".rgMasterTable"
