#! python3
# functional_tests.py

import os
import random
import unittest
from urllib.request import urlopen

from FanGraphs import leaders


@unittest.SkipTest
class TestMajorLeagueLeaderboards(unittest.TestCase):

    parser = leaders.MajorLeagueLeaderboards()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.browser.current_url

    @classmethod
    def tearDownClass(cls):
        cls.parser.quit()
        for file in os.listdir("dist"):
            os.remove(os.path.join("dist", file))
        os.rmdir("dist")

    def test_raise_exceptions(self):
        # Raise MajorLeagueLeaderboard.FilterNotFound
        with self.assertRaises(
            self.parser.InvalidFilterQuery
        ):
            self.parser.list_options("nonexistent query")
        with self.assertRaises(
            self.parser.InvalidFilterQuery
        ):
            self.parser.current_option("nonexistent query")
        with self.assertRaises(
            self.parser.InvalidFilterQuery
        ):
            self.parser.configure("nonexistent query", "nonexistent option")

    def test_init(self):
        res = urlopen(self.parser.address)
        self.assertEqual(res.getcode(), 200)

        self.assertTrue(self.parser.tree)

        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), "dist"))
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
            os.path.exists(os.path.join("dist", "test.csv"))
        )


class TestSplitsLeaderboards(unittest.TestCase):

    parser = leaders.SplitsLeaderboards()

    @classmethod
    def setUpClass(cls):
        cls.base_url = cls.parser.browser.current_url

    @classmethod
    def tearDownClass(cls):
        cls.parser.quit()
        for file in os.listdir("dist"):
            os.remove(os.path.join("dist", file))
        os.rmdir("dist")

    def test_init(self):
        self.assertTrue(self.parser.tree)
        self.assertTrue(self.parser.browser)
        self.assertTrue(os.path.exists("dist"))


if __name__ == "__main__":
    unittest.main()
