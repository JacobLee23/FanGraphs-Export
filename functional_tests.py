#! python3
# functional_tests.py

import random
import unittest

from FanGraphs import leaders


class TestMajorLeagueLeaderboards(unittest.TestCase):

    def setUp(self):
        self.parser = leaders.MajorLeagueLeaderboards()
        self.base_url = self.parser.browser.current_url

    def tearDown(self):
        self.parser.quit()

    def test_class(self):
        # Raise MajorLeagueLeaderboards.FilterNotFound
        with self.assertRaises(
            self.parser.InvalidFilterQuery
        ):
            self.parser.list_options("nonexistent option")

        # Test listquieres classmethod
        queries = self.parser.list_queries()
        self.assertIsInstance(queries, dict)
        self.assertEqual(
            list(queries),
            ["selection", "dropdown", "checkbox"]
        )
        self.assertTrue(
            all([isinstance(q, list) for q in queries.values()])
        )

        # Test listoptions classmethod
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

        # Test current_option classmethod
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

        # Test configure classmethod
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

        # Test reset classmethod
        self.parser.browser.get("https://google.com")
        self.parser.reset()
        self.assertEqual(
            self.parser.browser.current_url,
            self.base_url
        )


if __name__ == "__main__":
    unittest.main()
