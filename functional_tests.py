#! python3
# functional_tests.py

import unittest

from FanGraphs import leaders


class TestMajorLeagueLeaderboards(unittest.TestCase):

    def setUp(self):
        self.parser = leaders.MajorLeagueLeaderboards()

    def tearDown(self):
        self.parser.quit()

    def test_class(self):
        # Raise MajorLeagueLeaderboards.FilterNotFound
        with self.assertRaises(
            self.parser.FilterNotFound
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
                len(options)
            )


if __name__ == "__main__":
    unittest.main()
