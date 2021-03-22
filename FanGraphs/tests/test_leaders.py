#! python3
# tests/test_leaders.py

import unittest

import bs4
from playwright.sync_api import sync_playwright
import pytest
import requests


class TestMajorLeagueLeaderboards:

    __selections = {
        "group": "#LeaderBoard1_tsGroup",
        "stat": "#LeaderBoard1_tsStats",
        "position": "#LeaderBoard1_tsPosition",
        "type": "#LeaderBoard1_tsType"
    }
    __dropdowns = {
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
    __dropdown_options = {
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
    __checkboxes = {
        "split_teams": "#LeaderBoard1_cbTeams",
        "active_roster": "#LeaderBoard1_cbActive",
        "hof": "#LeaderBoard1_cbHOF",
        "split_seasons": "#LeaderBoard1_cbSeason",
        "rookies": "#LeaderBoard1_cbRookie"
    }
    __buttons = {
        "season1": "#LeaderBoard1_btnMSeason",
        "season2": "#LeaderBoard1_btnMSeason",
        "age1": "#LeaderBoard1_cmdAge",
        "age2": "#LeaderBoard1_cmdAge"
    }

    address = "https://fangraphs.com/leaders.aspx"

    @classmethod
    def setup_class(cls):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(cls.address, timeout=0)
            cls.soup = bs4.BeautifulSoup(
                page.content(), features="lxml"
            )
            browser.close()

    def test_address(self):
        res = requests.get(self.address)
        assert res.status_code == 200

    @pytest.mark.parametrize(
        "selectors",
        [__selections, __dropdowns, __dropdown_options,
         __checkboxes, __buttons]
    )
    def test_selectors(self, selectors: dict):
        for query, sel in selectors.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    @pytest.mark.parametrize(
        "selectors",
        [__selections, __dropdown_options]
    )
    def test_list_options(self, selectors: dict):
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} li")
            assert all([isinstance(e.getText(), str) for e in elems]), query

    def test_current_option_selections_selectors(self):
        for query, sel in self.__selections.items():
            elem = self.soup.select(f"{sel} .rtsLink.rtsSelected")
            assert len(elem) == 1, query
            assert isinstance(elem[0].getText(), str), query

    def test_current_option_dropdowns_selectors(self):
        for query, sel in self.__dropdowns.items():
            elem = self.soup.select(sel)[0]
            assert elem.get("value") is not None, query

    def test_expand_sublevel_selector(self):
        elems = self.soup.select("#LeaderBoard1_tsType a[href='#']")
        assert len(elems) == 1

    def test_export_selector(self):
        elems = self.soup.select("#LeaderBoard1_cmdCSV")
        assert len(elems) == 1


class TestSplitsLeaderboards:

    __selections = {
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
    __dropdowns = {
        "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
        "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
        "groupby": ".fg-dropdown.group-by"
    }
    __splits = {
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
    __quick_splits = {
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
    __switches = {
        "split_teams": "#stack-buttons > div:nth-child(2)",
        "auto_pt": "#stack-buttons > div:nth-child(3)"
    }

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    @classmethod
    def setup_class(cls):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(cls.address, timeout=0)
            cls.soup = bs4.BeautifulSoup(
                page.content(), features="lxml"
            )
            browser.close()

    def test_selections_selectors(self):
        for query, sel_list in self.__selections.items():
            for sel in sel_list:
                elems = self.soup.select(sel)
                assert len(elems) == 1, query

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns, __splits, __quick_splits, __switches]
    )
    def test_selectors(self, selectors: dict):
        for query, sel in selectors.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_reset_filters_selector(self):
        elems = self.soup.select("#stack-buttons .fgButton.small:nth-last-child(1)")
        assert len(elems) == 1

    def test_configure_filter_group_selector(self):
        groups = ["Quick Splits", "Splits", "Filters", "Show All"]
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        assert len(elems) == 4
        assert [e.getText() for e in elems] == groups

    def test_update_button_selector(self):
        elems = self.soup.select("#button-update")
        assert len(elems) == 0

    def test_current_option_selections(self):
        for query, sel_list in self.__selections.items():
            class_attrs = []
            for sel in sel_list:
                elem = self.soup.select(sel)[0]
                assert elem.get("class") is not None
                class_attrs.append(elem.get("class"))
            active = ["isActive" in a for a in class_attrs]
            assert active.count(True) == 1, query

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns, __splits, __switches]
    )
    def test_current_option(self, selectors: dict):
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} li")
            for elem in elems:
                assert elem.get("class") is not None

    def test_expand_table_dropdown_selector(self):
        elems = self.soup.select(".table-page-control:nth-child(3) select")
        assert len(elems) == 1

    def test_expand_table_dropdown_options_selector(self):
        options = ["30", "50", "100", "200", "Infinity"]
        elems = self.soup.select(".table-page-control:nth-child(3) select option")
        assert len(elems) == 5
        assert [e.getText() for e in elems] == options

    def test_table_headers_selector(self):
        elems = self.soup.select(".table-scroll thead tr th")
        assert len(elems) == 24

    def test_table_rows_selector(self):
        elems = self.soup.select(".table-scroll tbody tr")
        assert len(elems) == 30
        for elem in elems:
            assert len(elem.select("td")) == 24


class TestSeasonStatGrid(unittest.TestCase):

    address = "https://www.fangraphs.com/leaders/season-stat-grid"

    @classmethod
    def setUpClass(cls):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(cls.address, timeout=0)
            cls.soup = bs4.BeautifulSoup(
                page.content(), features="lxml"
            )
            browser.close()

    def test_base_address(self):
        self.assertEqual(
            requests.get(self.address).status_code, 200
        )

    def test_selections_selectors(self):
        selectors = {
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
        for cat in selectors:
            for sel in selectors[cat]:
                elems = self.soup.select(sel)
                self.assertEqual(
                    len(elems), 1, (cat, sel)
                )

    def test_dropdown_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_list_options_selections(self):
        selectors = {
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
        for cat in selectors:
            elems = [
                self.soup.select(sel)[0]
                for sel in selectors[cat]
            ]
            options = [e.getText() for e in elems]
            self.assertEqual(
                len(options), len(selectors[cat])
            )

    def test_list_options_dropdowns(self):
        selectors = {
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
        elem_count = {
            "start_season": 71, "end_season": 71, "popular": 6,
            "standard": 20, "advanced": 17, "statcast": 8, "batted_ball": 24,
            "win_probability": 10, "pitch_type": 25, "plate_discipline": 25,
            "value": 11
        }
        for cat in selectors:
            elems = self.soup.select(
                f"{selectors[cat]} li"
            )
            self.assertEqual(
                len(elems), elem_count[cat]
            )
            self.assertTrue(
                all([e.getText() for e in elems])
            )

    def test_current_option_selections(self):
        selector = "div[class='fgButton button-green active isActive']"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 2
        )

    def test_current_options_dropdowns(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(
                f"{selectors[cat]} li[class$='highlight-selection']"
            )
            if cat in ["start_season", "end_season", "popular", "value"]:
                self.assertEqual(
                    len(elems), 1, cat
                )
                self.assertIsNotNone(
                    elems[0].getText()
                )
            else:
                self.assertEqual(
                    len(elems), 0, cat
                )

    def test_expand_table_dropdown_selector(self):
        selector = ".table-page-control:nth-child(3) select"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 1
        )

    def test_expand_table_dropdown_options_selectors(self):
        options = ["30", "50", "100", "200", "Infinity"]
        selector = ".table-page-control:nth-child(3) select option"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 5
        )
        self.assertEqual(
            [e.getText() for e in elems], options
        )

    def test_sortby_option_selectors(self):
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 12
        )

    def test_write_table_headers_selector(self):
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 12
        )

    def test_write_table_rows_selector(self):
        selector = ".table-scroll tbody tr"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 30
        )
        for elem in elems:
            item_elems = elem.select("td")
            self.assertEqual(len(item_elems), 12)
