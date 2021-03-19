#! python3
# tests/leaders.py

import unittest

import bs4
from playwright.sync_api import sync_playwright
import requests


@unittest.SkipTest
class TestMajorLeagueLeaderboards(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.address = "https://fangraphs.com/leaders.aspx"
        cls.res = requests.get(cls.address)
        cls.soup = bs4.BeautifulSoup(cls.res.text)

    def test_selections_selectors(self):
        selectors = {
            "group": "#LeaderBoard1_tsGroup",
            "stat": "#LeaderBoard1_tsStats",
            "position": "#LeaderBoard1_tsPosition",
            "type": "#LeaderBoard1_tsType"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_dropdowns_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_dropdown_options_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_checkboxes_selectors(self):
        selectors = {
            "split_teams": "#LeaderBoard1_cbTeams",
            "active_roster": "#LeaderBoard1_cbActive",
            "hof": "#LeaderBoard1_cbHOF",
            "split_seasons": "#LeaderBoard1_cbSeason",
            "rookies": "#LeaderBoard1_cbRookie"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_buttons_selectors(self):
        selectors = {
            "season1": "#LeaderBoard1_btnMSeason",
            "season2": "#LeaderBoard1_btnMSeason",
            "age1": "#LeaderBoard1_cmdAge",
            "age2": "#LeaderBoard1_cmdAge"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_address(self):
        self.assertEqual(
            requests.get(self.address).status_code, 200
        )

    def test_list_options_dropdown_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(f"{selectors[cat]} li")
            self.assertTrue(
                all([isinstance(e.getText(), str) for e in elems])
            )

    def test_list_options_selections_selectors(self):
        selectors = {
            "group": "#LeaderBoard1_tsGroup",
            "stat": "#LeaderBoard1_tsStats",
            "position": "#LeaderBoard1_tsPosition",
            "type": "#LeaderBoard1_tsType"
        }
        for cat in selectors:
            elems = self.soup.select(f"{selectors[cat]} li")
            self.assertTrue(
                all([isinstance(e.getText(), str) for e in elems])
            )

    def test_current_option_checkbox_selectors(self):
        selectors = {
            "split_teams": "#LeaderBoard1_cbTeams",
            "active_roster": "#LeaderBoard1_cbActive",
            "hof": "#LeaderBoard1_cbHOF",
            "split_seasons": "#LeaderBoard1_cbSeason",
            "rookies": "#LeaderBoard1_cbRookie"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_current_option_dropdowns_selectors(self):
        selectors = {
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
        for cat in selectors:
            elem = self.soup.select(selectors[cat])[0]
            self.assertIsNotNone(
                elem.get("value")
            )

    def test_current_option_selections_selectors(self):
        selectors = {
            "group": "#LeaderBoard1_tsGroup",
            "stat": "#LeaderBoard1_tsStats",
            "position": "#LeaderBoard1_tsPosition",
            "type": "#LeaderBoard1_tsType"
        }
        for cat in selectors:
            elem = self.soup.select(f"{selectors[cat]} .rtsLink.rstSelected")
            self.assertEqual(
                len(elem), 1
            )
            self.assertIsInstance(elem.getText(), str)

    def test_configure_dropdown_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(f"{selectors[cat]} > div > ul > li")
            self.assertTrue(elems)

    def test_configure_selection_selectors(self):
        selectors = {
            "group": "#LeaderBoard1_tsGroup",
            "stat": "#LeaderBoard1_tsStats",
            "position": "#LeaderBoard1_tsPosition",
            "type": "#LeaderBoard1_tsType"
        }
        for cat in selectors:
            elems = self.soup.select(f"{selectors[cat]} li")
            self.assertTrue(elems)

    def test_configure_selection_expand_sublevel(self):
        elems = self.soup.select("#LeaderBoard_tsType a[href='#']")
        self.assertEqual(len(elems), 1)

    def test_export_id(self):
        elems = self.soup.select("#LeaderBoard1_cmdCSV")
        self.assertEqual(len(elems), 1)


class TestSplitsLeaderboards(unittest.TestCase):

    play = sync_playwright().start()
    browser = play.chromium.launch()
    page = browser.new_page()

    @classmethod
    def setUpClass(cls):
        cls.address = "https://www.fangraphs.com/leaders/splits-leaderboards"
        cls.page.goto(cls.address)
        cls.soup = bs4.BeautifulSoup(
            cls.page.content(), features="lxml"
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.play.stop()

    def test_selections_selectors(self):
        selectors = {
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
        for cat in selectors:
            for sel in selectors[cat]:
                elems = self.soup.select(sel)
                self.assertEqual(
                    len(elems), 1, (cat, sel)
                )

    def test_dropdowns_selectors(self):
        selectors = {
            "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
            "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
            "groupby": ".fg-dropdown.group-by"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_splits_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_quick_splits_selectors(self):
        selectors = {
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
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_switches_selectors(self):
        selectors = {
            "split_teams": "#stack-buttons > div:nth-child(2)",
            "auto_pt": "#stack-buttons > div:nth-child(3)"
        }
        for cat in selectors:
            elems = self.soup.select(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_reset_filters_selector(self):
        selector = "#stack-buttons div[class='fgButton small']:nth-last-child(1)"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 1
        )

    def test_configure_filter_group_selector(self):
        groups = ["Quick Splits", "Splits", "Filters", "Show All"]
        selector = ".fgBin.splits-bin-controller div"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 4
        )
        self.assertEqual(
            [e.getText() for e in elems], groups
        )

    def test_update_button_selector(self):
        selector = "#button-update"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 0
        )

    def test_current_option_selections(self):
        selectors = {
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
        for query in selectors:
            class_attributes = []
            for sel in selectors[query]:
                elem = self.soup.select(sel)[0]
                self.assertTrue(elem.get("class"))
                class_attributes.append(elem.get("class"))
            self.assertEqual(
                ["isActive" in attr for attr in class_attributes].count(True),
                1
            )

    def test_current_option_dropdowns(self):
        selectors = {
            "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
            "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
            "groupby": ".fg-dropdown.group-by"
        }
        for query in selectors:
            elems = self.soup.select(f"{selectors[query]} ul li")
            for elem in elems:
                self.assertTrue(elem.get("class"))

    def test_current_option_splits(self):
        selectors = {
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
        for query in selectors:
            elems = self.soup.select(f"{selectors[query]} ul li")
            for elem in elems:
                self.assertTrue(elem.get("class"))

    def test_current_option_switches(self):
        selectors = {
            "split_teams": "#stack-buttons > div:nth-child(2)",
            "auto_pt": "#stack-buttons > div:nth-child(3)"
        }
        for query in selectors:
            elem = self.soup.select(selectors[query])[0]
            self.assertTrue(elem.get("class"))

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
            len(elems), 24
        )

    def test_write_table_headers_selector(self):
        selector = ".table-scroll thead tr th"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 24
        )

    def test_write_table_rows_selector(self):
        selector = ".table-scroll tbody tr"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 30
        )
        for elem in elems:
            item_elems = elem.select("td")
            self.assertEqual(len(item_elems), 24)


@unittest.SkipTest
class TestSeasonStatGrid(unittest.TestCase):

    play = sync_playwright().start()
    browser = play.chromium.launch()
    page = browser.new_page()

    @classmethod
    def setUpClass(cls):
        cls.address = "https://www.fangraphs.com/leaders/season-stat-grid"
        cls.page.goto(cls.address)
        cls.soup = bs4.BeautifulSoup(
            cls.page.content(), features="lxml"
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.play.stop()

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


if __name__ == "__main__":
    unittest.main()
