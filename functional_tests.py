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
            self.parser.listoptions("nonexistent option")

        # Test listoptions classmethod
        queries = {
            "group": 3, "stat": 3, "position": 13,
            "league": 3, "team": 31, "single_season": 151, "split": 67,
            "min_pa": 60, "season1": 151, "season2": 151, "age1": 45, "age2": 45,
            "split_teams": 2, "active_roster": 2, "hof": 2, "split_seasons": 2,
            "rookies": 2
        }
        for query in queries:
            self.assertEqual(
                len(self.parser.listoptions(query)),
                queries[query],
                len(self.parser.listoptions(query))
            )


if __name__ == "__main__":
    unittest.main()
