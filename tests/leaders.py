#! python3
# tests/leaders.py

import unittest
from urllib.request import urlopen

from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


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


class TestSeasonStatGrid(unittest.TestCase):

    browser = webdriver.Firefox()

    @classmethod
    def setUpClass(cls):
        cls.address = "https://www.fangraphs.com/leaders/season-stat-grid"
        cls.browser.get(cls.address)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

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
                elems = self.browser.find_elements_by_css_selector(sel)
                self.assertEqual(
                    len(elems), 1, (cat, sel)
                )

    def test_dropdown_selectors(self):
        selectors = {
            "start_season": "div.row-season div:nth-child(2)",
            "end_season": "div.row-season div:nth-child(4)"
        }
        for cat in selectors:
            elems = self.browser.find_elements_by_css_selector(selectors[cat])
            self.assertEqual(
                len(elems), 1, cat
            )

    def test_dropdown_options_selectors(self):
        selectors = {
            "start_season": "div.row-season div:nth-child(2) ul li",
            "end_season": "div.row-season div:nth-child(4) ul li"
        }
        for cat in selectors:
            elems = self.browser.find_elements_by_css_selector(
                selectors[cat]
            )
            self.assertEqual(
                len(elems), 71, cat
            )


if __name__ == "__main__":
    unittest.main()
