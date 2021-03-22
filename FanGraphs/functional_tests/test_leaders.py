#! python3
# functional_tests/test_leaders.py

import csv
import os
import random
import unittest

import pytest
import requests

from .. import exceptions
from .. import leaders


class TestExceptions:

    @pytest.mark.parametrize(
        "page_class",
        [leaders.MajorLeagueLeaderboards,
         leaders.SplitsLeaderboards,
         leaders.SeasonStatGrid]
    )
    def test_class_exceptions(self, page_class):
        with pytest.raises(exceptions.UnknownBrowserException):
            page_class(browser="nonexistent browser")
        parser = page_class()

        with pytest.raises(exceptions.InvalidFilterQueryException):
            parser.list_options("nonexistent query")
        with pytest.raises(exceptions.InvalidFilterQueryException):
            parser.current_option("nonexistent query")
        with pytest.raises(exceptions.InvalidFilterQueryException):
            parser.configure("nonexistent query", "nonexistent option")
        with pytest.raises(exceptions.InvalidFilterOptionException):
            parser.configure("Type", "nonexistent option")

        parser.quit()


class TestMajorLeagueLeaderboards:

    parser = leaders.MajorLeagueLeaderboards()

    @classmethod
    def setup_class(cls):
        cls.base_url = cls.parser.page.url

    @classmethod
    def teardown_class(cls):
        cls.parser.quit()
        for file in os.listdir("out"):
            os.remove(os.path.join("out", file))
        os.rmdir("out")
        os.system("taskkill /F /IM firefox.exe")

    def test_init(self):
        res = requests.get(self.parser.address)
        assert res.status_code == 200
        assert self.parser.page
        assert self.parser.soup

    def test_list_queries(self):
        queries = self.parser.list_queries()
        assert isinstance(queries, list)
        assert all([isinstance(q, str) for q in queries])

    def test_list_options(self):
        query_count = {
            "group": 3, "stat": 3, "position": 13,
            "league": 3, "team": 31, "single_season": 151, "split": 67,
            "min_pa": 60, "season1": 151, "season2": 151, "age1": 45, "age2": 45,
            "split_teams": 2, "active_roster": 2, "hof": 2, "split_seasons": 2,
            "rookies": 2
        }
        for query in query_count:
            options = self.parser.list_options(query)
            assert isinstance(options, list)
            assert all([isinstance(o, (list, bool)) for o in options])
            assert len(options) == query_count[query], query

    def test_current_option(self):
        query_options = {
            "group": "Player Stats", "stat": "Batting", "position": "All",
            "league": "All Leagues", "team": "All Teams", "single_season": "2020",
            "split": "Full Season", "min_pa": "Qualified", "season1": "2020",
            "season2": "2020", "age1": "14", "age2": "58", "split_teams": "False",
            "active_roster": "False", "hof": "False", "split_seasons": "False",
            "rookies": "False"
        }
        for query in query_options:
            option = self.parser.current_option(query)
            assert option == query_options[query], query

    def test_configure(self):
        queries = [
            "group", "stat", "position", "league", "team", "single_season",
            "split", "min_pa", "season1", "season2", "age1", "age2",
            "split_teams", "active_roster", "hof", "split_seasons", "rookies"
        ]
        for query in queries:
            option = random.choice(self.parser.list_options(query))
            self.parser.configure(query, option)
            if query not in ["season1", "season2", "age1", "age2"]:
                current = self.parser.current_option(query)
                assert option == current, query
            self.parser.reset()

    def test_reset(self):
        self.parser.page.goto("https://google.com")
        self.parser.reset()
        assert self.parser.page.url == self.base_url

    def test_export(self):
        self.parser.export("test.csv")
        assert os.path.exists(os.path.join("out", "test.csv"))


class TestSplitsLeaderboards(unittest.TestCase):

    parser = leaders.SplitsLeaderboards()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.page.url

    @classmethod
    def tearDownClass(cls):
        cls.parser.quit()
        for file in os.listdir("out"):
            os.remove(os.path.join("out", file))
        os.rmdir("out")
        os.system("taskkill /F /IM firefox.exe")

    def test_00(self):
        """
        SplitsLeaderboards.__init__
        """
        self.assertEqual(
            requests.get(self.parser.address).status_code, 200
        )
        self.assertTrue(os.path.exists("out"))
        self.assertTrue(self.parser.page)
        self.assertTrue(self.parser.soup)

    def test_01(self):
        """
        SplitsLeaderboards.list_queries
        """
        # SeasonStatGrid.list_queries
        self.assertEqual(
            len(self.parser.list_queries()), 20
        )

    def test_02(self):
        """
        SplitsLeaderboards.list_filter_groups
        """
        groups = self.parser.list_filter_groups()
        self.assertEqual(
            len(groups), 4
        )
        self.assertEqual(
            groups, ["Quick Splits", "Splits", "Filters", "Show All"]
        )

    def test_03(self):
        """
        SplitsLeaderboards.list_options
        """
        option_count = {
            "group": 4, "stat": 2, "type": 3,
            "time_filter": 10, "preset_range": 12, "groupby": 5,
            "handedness": 4, "home_away": 2, "batted_ball": 15,
            "situation": 7, "count": 11, "batting_order": 9, "position": 12,
            "inning": 10, "leverage": 3, "shifts": 3, "team": 32,
            "opponent": 32,
            "split_teams": 2, "auto_pt": 2
        }
        for query in option_count:
            self.assertEqual(
                len(self.parser.list_options(query)), option_count[query],
                query
            )

    def test_04(self):
        """
        SplitsLeaderboards.current_option
        """
        current_options = {
            "group": ["Player"], "stat": ["Batting"], "type": ["Standard"],
            "time_filter": [], "preset_range": [], "groupby": ["Season"],
            "handedness": [], "home_away": [], "batted_ball": [],
            "situation": [], "count": [], "batting_order": [], "position": [],
            "inning": [], "leverage": [], "shifts": [], "team": [],
            "opponent": [],
            "split_teams": ["False"], "auto_pt": ["False"]
        }
        for query in current_options:
            self.assertEqual(
                self.parser.current_option(query), current_options[query],
                query
            )

    def test_05(self):
        """
        SplitsLeaderboards.configure
        """
        queries = self.parser.list_queries()
        for query in queries:
            if query in ["type"]:
                continue
            option = self.parser.list_options(query)[-1]
            self.parser.configure(query, option, autoupdate=True)
            self.assertIn(
                option, self.parser.current_option(query),
                query
            )
            self.parser.reset()

    def test_06(self):
        """
        SplitsLeaderboards.list_quick_splits
        """
        quick_splits = [
            'batting_home', 'batting_away', 'vs_lhp', 'vs_lhp_home',
            'vs_lhp_away', 'vs_lhp_as_lhh', 'vs_lhp_as_rhh', 'vs_rhp',
            'vs_rhp_home', 'vs_rhp_away', 'vs_rhp_as_lhh', 'vs_rhp_as_rhh',
            'pitching_as_sp', 'pitching_as_rp', 'pitching_home',
            'pitching_away', 'vs_lhh', 'vs_lhh_home', 'vs_lhh_away',
            'vs_lhh_as_rhp', 'vs_lhh_as_lhp', 'vs_rhh', 'vs_rhh_home',
            'vs_rhh_away', 'vs_rhh_as_rhp', 'vs_rhh_as_lhp'
        ]
        self.assertEqual(
            self.parser.list_quick_splits(), quick_splits
        )

    def test_07(self):
        """
        SplitsLeaderboards.configure_quick_split
        """
        for qsplit in self.parser.list_quick_splits():
            self.parser.configure_quick_split(qsplit)
            self.assertTrue(
                self.parser.current_option("handedness"),
                qsplit
            )

    def test_08(self):
        """
        SplitsLeaderboards.export
        """
        self.parser.export("test.csv", size="30")
        self.assertTrue(
            os.path.exists(
                os.path.join("out", "test.csv")
            )
        )


class TestSeasonStatGrid(unittest.TestCase):

    parser = leaders.SeasonStatGrid()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.page.url

    @classmethod
    def tearDownClass(cls):
        for file in os.listdir("out"):
            os.remove(os.path.join("out", file))
        os.rmdir("out")
        cls.parser.quit()
        os.system("taskkill /F /IM firefox.exe")

    def test_init(self):
        self.assertEqual(
            requests.get(self.parser.address).status_code, 200
        )
        self.assertTrue(os.path.exists("out"))
        self.assertTrue(self.parser.page)
        self.assertTrue(self.parser.soup)

    def test_list_queries(self):
        self.assertEqual(
            len(self.parser.list_queries()), 13
        )

    def test_list_options(self):
        option_count = {
            "stat": 2, "type": 3, "start_season": 71, "end_season": 71,
            "popular": 6, "standard": 20, "advanced": 17, "statcast": 8,
            "batted_ball": 24, "win_probability": 10, "pitch_type": 25,
            "plate_discipline": 25, "value": 11
        }
        for query in option_count:
            self.assertEqual(
                len(self.parser.list_options(query)), option_count[query],
                query
            )

    def test_current_option(self):
        current_options = {
            "stat": "Batting", "type": "Normal", "start_season": "2011",
            "end_season": "2020", "popular": "WAR", "standard": "None",
            "advanced": "None", "statcast": "None", "batted_ball": "None",
            "win_probability": "None", "pitch_type": "None",
            "plate_discipline": "None", "value": "WAR"
        }
        for query in current_options:
            self.assertEqual(
                self.parser.current_option(query), current_options[query],
                query
            )

    def test_configure(self):
        self.parser.reset()
        queries = self.parser.list_queries()
        for query in queries:
            option = self.parser.list_options(query)[-1]
            self.parser.configure(query, option)
            if query not in ["end_season"]:
                self.assertEqual(
                    self.parser.current_option(query), option,
                    query
                )
            self.parser.reset()

    def test_export(self):
        self.parser.reset()
        self.parser.export("test.csv", size="30")
        self.assertTrue(
            os.path.exists(os.path.join("out", "test.csv"))
        )
        with open(os.path.join("out", "test.csv")) as file:
            reader = csv.reader(file)
            data = list(reader)
        self.assertEqual(
            len(data), 31
        )
        self.assertTrue(
            all([len(r) == 12 for r in data])
        )

    def test_reset(self):
        self.parser.page.goto("https://google.com")
        self.parser.reset()
        self.assertEqual(
            self.parser.page.url,
            self.base_url
        )


if __name__ == "__main__":
    unittest.main()
