#! python3
# functional_tests.py

import csv
import os
import random
import requests
import unittest

from FanGraphs import exceptions
from FanGraphs import leaders


@unittest.skip
class TestExceptions(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        os.system("taskkill /F /IM firefox.exe")

    def test_major_league_leaderboards(self):
        parser = leaders.MajorLeagueLeaderboards()

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.list_options("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.current_option("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.configure("nonexistent query", "nonexistent option")

        parser.quit()

    def test_season_stat_grid(self):
        parser = leaders.SeasonStatGrid()

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.list_options("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.current_option("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQueryException
        ):
            parser.configure("nonexistent query", "nonexistent option")

        with self.assertRaises(
            exceptions.InvalidFilterOptionException
        ):
            parser.configure("Stat", "nonexistent option")

        parser.quit()


@unittest.skip
class TestMajorLeagueLeaderboards(unittest.TestCase):

    parser = leaders.MajorLeagueLeaderboards()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.browser.current_url

    @classmethod
    def tearDownClass(cls):
        cls.parser.quit()
        for file in os.listdir("out"):
            os.remove(os.path.join("out", file))
        os.rmdir("out")
        os.system("taskkill /F /IM firefox.exe")

    def test_init(self):
        self.assertEqual(
            requests.get(self.parser.address).status_code, 200
        )
        self.assertTrue(self.parser.tree)
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), "out"))
        )
        self.assertTrue(self.parser.browser)

    def test_list_queries(self):
        queries = self.parser.list_queries()
        self.assertIsInstance(queries, list)
        self.assertTrue(
            all([isinstance(q, str) for q in queries])
        )

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
            self.assertIsInstance(options, list)
            self.assertTrue(
                all([isinstance(o, str) for o in options])
                or all([isinstance(o, bool) for o in options])
            )
            self.assertEqual(
                len(options),
                query_count[query],
                (query, len(options))
            )

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
            self.assertEqual(
                option,
                query_options[query],
                (query, option)
            )

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
                self.assertEqual(
                    option,
                    current,
                    (query, option, current)
                )
            self.parser.reset()

    def test_reset(self):
        self.parser.browser.get("https://google.com")
        self.parser.reset()
        self.assertEqual(
            self.parser.browser.current_url,
            self.base_url
        )

    def test_export(self):
        self.parser.export("test.csv")
        self.assertTrue(
            os.path.exists(os.path.join("out", "test.csv"))
        )


class TestSplitsLeaderboards(unittest.TestCase):

    parser = leaders.SplitsLeaderboards()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.browser.current_url

    @classmethod
    def tearDownClass(cls):
        cls.parser.quit()
        # for file in os.listdir("out"):
        #    os.remove(os.path.join("out", file))
        # os.rmdir("out")
        os.system("taskkill /F /IM firefox.exe")

    @unittest.SkipTest
    def test_init(self):
        self.assertEqual(
            requests.get(self.parser.address).status_code, 200
        )
        self.assertTrue(os.path.exists("out"))
        self.assertTrue(self.parser.browser)
        self.assertTrue(self.parser.soup)

    @unittest.SkipTest
    def test_list_queries(self):
        self.assertEqual(
            len(self.parser.list_queries()), 24
        )

    @unittest.SkipTest
    def test_list_filter_groups(self):
        groups = self.parser.list_filter_groups()
        self.assertEqual(
            len(groups), 4
        )
        self.assertEqual(
            groups, ["Quick Splits", "Splits", "Filters", "Show All"]
        )

    @unittest.SkipTest
    def test_list_options(self):
        option_count = {
            "group": 4, "stat": 2, "type": 3,
            "time_filter": 10, "preset_range": 12, "groupby": 5,
            "batting_ha": 2, "batting_v_lhp": 5, "batting_v_rhp": 5,
            "pitching_as_sprp": 2, "pitching_ha": 2, "pitching_v_lhh": 5,
            "pitching_v_rhh": 5,
            "handedness": 4, "home_away": 2, "batted_ball": 15,
            "situation": 7, "count": 11, "batting_order": 9, "position": 12,
            "inning": 10, "leverage": 3, "shifts": 3, "team": 32,
            "opponent": 32
        }
        for query in option_count:
            self.assertEqual(
                len(self.parser.list_options(query)), option_count[query],
                query
            )

    @unittest.SkipTest
    def test_current_option(self):
        current_options = {
            "group": ["Player"], "stat": ["Batting"], "type": ["Standard"],
            "time_filter": [], "preset_range": [], "groupby": ["Season"],
            "handedness": [], "home_away": [], "batted_ball": [],
            "situation": [], "count": [], "batting_order": [], "position": [],
            "inning": [], "leverage": [], "shifts": [], "team": [],
            "opponent": []
        }
        for query in current_options:
            self.assertEqual(
                self.parser.current_option(query), current_options[query],
                query
            )

    @unittest.SkipTest
    def test_configure(self):
        queries = self.parser.list_queries()
        for query in queries:
            option = self.parser.list_options(query)[-1]
            self.parser.configure(query, option, autoupdate=True)
            self.assertIn(
                option, self.parser.current_option(query),
                query
            )
            self.parser.reset()

    @unittest.SkipTest
    def test_quick_split(self):
        quick_splits = {
            'batting_home': 2, 'batting_away': 2, 'vs_lhp': 2, 'vs_lhp_home': 3,
            'vs_lhp_away': 3, 'vs_lhp_as_lhh': 3, 'vs_lhp_as_rhh': 3, 'vs_rhp': 2,
            'vs_rhp_home': 3, 'vs_rhp_away': 3, 'vs_rhp_as_lhh': 3, 'vs_rhp_as_rhh': 3,
            'pitching_as_sp': 2, 'pitching_as_rp': 2, 'pitching_home': 2,
            'pitching_away': 2, 'vs_lhh': 2, 'vs_lhh_home': 3, 'vs_lhh_away': 3,
            'vs_lhh_as_rhp': 3, 'vs_lhh_as_lhp': 3, 'vs_rhh': 2, 'vs_rhh_home': 3,
            'vs_rhh_away': 3, 'vs_rhh_as_rhp': 3, 'vs_rhh_as_lhp': 3
        }
        for qsplit in quick_splits:
            configs = self.parser.quick_split(qsplit)
            self.assertEqual(
                len(configs), quick_splits[qsplit],
                qsplit
            )

    @unittest.SkipTest
    def test_configure_quick_split(self):
        quick_splits = [
            'batting_home', 'batting_away', 'vs_lhp', 'vs_lhp_home',
            'vs_lhp_away', 'vs_lhp_as_lhh', 'vs_lhp_as_rhh', 'vs_rhp',
            'vs_rhp_home', 'vs_rhp_away', 'vs_rhp_as_lhh', 'vs_rhp_as_rhh',
            'pitching_as_sp', 'pitching_as_rp', 'pitching_home',
            'pitching_away', 'vs_lhh', 'vs_lhh_home', 'vs_lhh_away',
            'vs_lhh_as_rhp', 'vs_lhh_as_lhp', 'vs_rhh', 'vs_rhh_home',
            'vs_rhh_away', 'vs_rhh_as_rhp', 'vs_rhh_as_lhp'
        ]
        for qsplit in quick_splits:
            self.parser.configure_quick_split(qsplit)
            configurations = self.parser.quick_split(qsplit)
            for query, option in configurations:
                self.assertIn(
                    option, self.parser.current_option(query),
                    query
                )

    def test_export(self):
        self.parser.export("test.csv")
        self.assertTrue(
            os.path.exists(
                os.path.join("out", "test.csv")
            )
        )


@unittest.skip
class TestSeasonStatGrid(unittest.TestCase):

    parser = leaders.SeasonStatGrid()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.browser.current_url

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
        self.assertTrue(self.parser.browser)
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
        self.parser.browser.get("https://google.com")
        self.parser.reset()
        self.assertEqual(
            self.parser.browser.current_url,
            self.base_url
        )


if __name__ == "__main__":
    unittest.main()
