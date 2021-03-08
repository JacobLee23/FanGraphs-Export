#! python3
# functional_tests.py

import csv
import os
import random
import unittest
from urllib.request import urlopen

from FanGraphs import exceptions
from FanGraphs import leaders


class TestExceptions(unittest.TestCase):

    def test_major_league_leaderboards(self):
        parser = leaders.MajorLeagueLeaderboards()

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.list_options("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.current_option("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.configure("nonexistent query", "nonexistent option")

        parser.quit()

    def test_season_stat_grid(self):
        parser = leaders.SeasonStatGrid()

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.list_options("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.current_option("nonexistent query")

        with self.assertRaises(
            exceptions.InvalidFilterQuery
        ):
            parser.configure("nonexistent query", "nonexistent option")

        with self.assertRaises(
            exceptions.InvalidFilterOption
        ):
            parser.configure("Stat", "nonexistent option")

        parser.quit()


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

    def test_init(self):
        res = urlopen(self.parser.address)
        self.assertEqual(res.getcode(), 200)

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

    def test_init(self):
        self.assertEqual(
            urlopen(self.parser.address).getcode(), 200
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
