#! python3
# tests/leaders.py

import unittest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class TestMajorLeagueLeaderboards(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.headless = False
        self.browser = webdriver.Firefox(
            options=options
        )

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
