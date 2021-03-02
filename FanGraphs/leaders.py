#! python3
# FanGraphs/leaders.py

"""

"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class MajorLeagueLeaderboards:
    """ Parse FanGraphs >> Leaders >> Major League Leaderboards
"""
    def __init__(self):
        self.__options = Options()
        self.__options.headless = True
        self.browser = webdriver.Firefox(
            options=self.__options
        )

    def quit(self):
        self.browser.quit()


class SplitsLeaderboards:

    def __init__(self):
        pass


class SeasonStatGrid:

    def __init__(self):
        pass


class GameSpanLeaderboards:

    def __init__(self):
        pass


class KBOLeaderboards:

    def __init__(self):
        pass


class WARLeaderboards:

    def __init__(self):
        pass
