#! python3
# tests/leaders.py

import os
import unittest
from urllib.request import urlopen

import bs4
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


@unittest.SkipTest
class TestMajorLeagueLeaderboards(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.address = "https://fangraphs.com/leaders.aspx"
        cls.response = urlopen(cls.address)
        cls.parser = etree.HTMLParser()
        cls.tree = etree.parse(cls.response, cls.parser)

    def test_selections_ids(self):
        ids = [
            "LeaderBoard1_tsGroup",
            "LeaderBoard1_tsStats",
            "LeaderBoard1_tsPosition",
            "LeaderBoard1_tsType"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_dropdowns_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_Input",
            "LeaderBoard1_rcbTeam_Input",
            "LeaderBoard1_rcbSeason_Input",
            "LeaderBoard1_rcbMonth_Input",
            "LeaderBoard1_rcbMin_Input",
            "LeaderBoard1_rcbSeason1_Input",
            "LeaderBoard1_rcbSeason2_Input",
            "LeaderBoard1_rcbAge1_Input",
            "LeaderBoard1_rcbAge2_Input"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//input[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_dropdown_options_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_DropDown",
            "LeaderBoard1_rcbTeam_DropDown",
            "LeaderBoard1_rcbSeason_DropDown",
            "LeaderBoard1_rcbMonth_DropDown",
            "LeaderBoard1_rcbMin_DropDown",
            "LeaderBoard1_rcbSeason1_DropDown",
            "LeaderBoard1_rcbSeason2_DropDown",
            "LeaderBoard1_rcbAge1_DropDown",
            "LeaderBoard1_rcbAge2_DropDown"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_checkboxes_ids(self):
        ids = [
            "LeaderBoard1_cbTeams",
            "LeaderBoard1_cbActive",
            "LeaderBoard1_cbHOF",
            "LeaderBoard1_cbSeason",
            "LeaderBoard1_cbRookie"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//input[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_buttons_ids(self):
        ids = [
            "LeaderBoard1_btnMSeason",
            "LeaderBoard1_cmdAge"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//input[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_base_url(self):
        self.assertEqual(
            urlopen("https://fangraphs.com/leaders.aspx").getcode(),
            200
        )

    def test_list_options_dropdown_options_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_DropDown",
            "LeaderBoard1_rcbTeam_DropDown",
            "LeaderBoard1_rcbSeason_DropDown",
            "LeaderBoard1_rcbMonth_DropDown",
            "LeaderBoard1_rcbMin_DropDown",
            "LeaderBoard1_rcbSeason1_DropDown",
            "LeaderBoard1_rcbSeason2_DropDown",
            "LeaderBoard1_rcbAge1_DropDown",
            "LeaderBoard1_rcbAge2_DropDown"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']//div//ul//li"
            )
            self.assertTrue(elems)
            elem_text = [e.text for e in elems]
            self.assertTrue(
                all([isinstance(t, str) for t in elem_text])
            )

    def test_list_options_selections_ids(self):
        ids = [
            "LeaderBoard1_tsGroup",
            "LeaderBoard1_tsStats",
            "LeaderBoard1_tsPosition",
            "LeaderBoard1_tsType"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']//div//ul//li//a//span//span//span"
            )
            self.assertTrue(elems)
            elem_text = [e.text for e in elems]
            self.assertTrue(
                all([isinstance(t, str) for t in elem_text])
            )

    def test_current_option_checkbox_ids(self):
        ids = [
            "LeaderBoard1_cbTeams",
            "LeaderBoard1_cbActive",
            "LeaderBoard1_cbHOF",
            "LeaderBoard1_cbSeason",
            "LeaderBoard1_cbRookie"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//input[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1, len(elems)
            )

    def test_current_option_dropdowns_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_Input",
            "LeaderBoard1_rcbTeam_Input",
            "LeaderBoard1_rcbSeason_Input",
            "LeaderBoard1_rcbMonth_Input",
            "LeaderBoard1_rcbMin_Input",
            "LeaderBoard1_rcbSeason1_Input",
            "LeaderBoard1_rcbSeason2_Input",
            "LeaderBoard1_rcbAge1_Input",
            "LeaderBoard1_rcbAge2_Input"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//input[@id='{i}']"
            )
            self.assertEqual(
                len(elems), 1
            )
            self.assertIsNotNone(
                elems[0].get("value")
            )

    def test_current_option_selections_ids(self):
        ids = [
            "LeaderBoard1_tsGroup",
            "LeaderBoard1_tsStats",
            "LeaderBoard1_tsPosition",
            "LeaderBoard1_tsType"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']//div//ul//li//a[@class='rtsLink rtsSelected']//span//span//span"
            )
            self.assertEqual(
                len(elems), 1
            )

    def test_config_dropdown_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_Input",
            "LeaderBoard1_rcbTeam_Input",
            "LeaderBoard1_rcbSeason_Input",
            "LeaderBoard1_rcbMonth_Input",
            "LeaderBoard1_rcbMin_Input",
            "LeaderBoard1_rcbSeason1_Input",
            "LeaderBoard1_rcbSeason2_Input",
            "LeaderBoard1_rcbAge1_Input",
            "LeaderBoard1_rcbAge2_Input"
        ]
        for i in ids:
            elems = self.tree.xpath("//@id")
            self.assertIn(i, elems)
            self.assertEqual(
                elems.count(i), 1, elems.count(i)
            )

    def test_config_dropdown_options_ids(self):
        ids = [
            "LeaderBoard1_rcbLeague_DropDown",
            "LeaderBoard1_rcbTeam_DropDown",
            "LeaderBoard1_rcbSeason_DropDown",
            "LeaderBoard1_rcbMonth_DropDown",
            "LeaderBoard1_rcbMin_DropDown",
            "LeaderBoard1_rcbSeason1_DropDown",
            "LeaderBoard1_rcbSeason2_DropDown",
            "LeaderBoard1_rcbAge1_DropDown",
            "LeaderBoard1_rcbAge2_DropDown"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']//div//ul//li"
            )
            self.assertTrue(elems)

    def test_config_selection_ids(self):
        ids = [
            "LeaderBoard1_tsGroup",
            "LeaderBoard1_tsStats",
            "LeaderBoard1_tsPosition",
            "LeaderBoard1_tsType"
        ]
        for i in ids:
            elems = self.tree.xpath(
                f"//div[@id='{i}']//div//ul//li"
            )
            self.assertTrue(elems)

    def test_submit_form_id(self):
        ids = [
            "LeaderBoard1_btnMSeason",
            "LeaderBoard1_cmdAge"
        ]
        for i in ids:
            elems = self.tree.xpath("//@id")
            self.assertIn(i, elems)
            self.assertEqual(
                elems.count(i), 1, elems.count(i)
            )

    def test_export_id(self):
        self.assertIn(
            "LeaderBoard1_cmdCSV",
            self.tree.xpath("//@id")
        )


class TestSplitsLeaderboards(unittest.TestCase):

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    @classmethod
    def setUpClass(cls):
        cls.address = "https://www.fangraphs.com/leaders/splits-leaderboards"
        cls.browser.get(cls.address)
        WebDriverWait(
            cls.browser, 5
        ).until(expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, "#react-drop-test div")
        ))
        cls.soup = bs4.BeautifulSoup(
            cls.browser.page_source, features="lxml"
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        os.system("taskkill /F /IM firefox.exe")

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

    def test_export_data_classname(self):
        selector = ".data-export"
        elems = self.soup.select(selector)
        self.assertEqual(
            len(elems), 1
        )


@unittest.SkipTest
class TestSeasonStatGrid(unittest.TestCase):

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    @classmethod
    def setUpClass(cls):
        cls.address = "https://www.fangraphs.com/leaders/season-stat-grid"
        cls.browser.get(cls.address)
        WebDriverWait(
            cls.browser, 5
        ).until(expected_conditions.presence_of_element_located(
            (By.ID, "root-season-grid")
        ))
        cls.soup = bs4.BeautifulSoup(
            cls.browser.page_source, features="lxml"
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        os.system("taskkill /F /IM firefox.exe")

    def test_base_address(self):
        self.assertEqual(
            urlopen(self.address).getcode(), 200
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
