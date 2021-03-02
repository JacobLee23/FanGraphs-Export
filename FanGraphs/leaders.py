#! python3
# FanGraphs/leaders.py

"""

"""

from urllib.request import urlopen

from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class MajorLeagueLeaderboards:
    """ Parse FanGraphs >> Leaders >> Major League Leaderboards
"""
    def __init__(self):
        self.__selections = {
            "group": "//div[@id='LeaderBoard1_tsGroup']",
            "stats": "//div[@id='LeaderBoard1_tsStats']",
            "position": "//div[@id='LeaderBoard1_tsPosition']",
        }
        self.__dropdowns = {
            "league": "//div[@id='LeaderBoard1_rcbLeague']",
            "teams": "//div[@id='LeaderBoard1_rcbTeam']",
            "single_season": "//div[@id='LeaderBoard1_rcbSeason']",
            "split": "//div[@id='LeaderBoard1_rcbMonth']",
            "min_pa": "//div[@id='LeaderBoard1_rcbMin']",
            "season1": "//div[@id='LeaderBoard1_rcbSeason1']",
            "season2": "//div[@id='LeaderBoard1_rcbSeason2']",
            "age1": "//div[@id='LeaderBoard1_rcbAge1']",
            "age2": "//div[@id='LeaderBoard1_rcbAge2']"
        }
        self.__dropdown_options = {
            "league": "//div[@id='LeaderBoard1_rcbLeague_DropDown']",
            "teams": "//div[@id='LeaderBoard1_rcbTeam_DropDown']",
            "single_season": "//div[@id='LeaderBoard1_rcbSeason_DropDown']",
            "split": "//div[@id='LeaderBoard1_rcbMonth_DropDown']",
            "min_pa": "//div[@id='LeaderBoard1_rcbMin_DropDown']",
            "season1": "//div[@id='LeaderBoard1_rcbSeason1_DropDown']",
            "season2": "//div[@id='LeaderBoard1_rcbSeason2_DropDown']",
            "age1": "//div[@id='LeaderBoard1_rcbAge1_DropDown']",
            "age2": "//div[@id='LeaderBoard1_rcbAge2_DropDown']"
        }
        self.__checkboxes = {
            "split_teams": "//input[@id='LeaderBoard1_cbTeams']",
            "active_roster": "//input[@id='LeaderBoard1_cbActive']",
            "hof": "//input[@id='LeaderBoard1_cbHOF']",
            "split_seasons": "//input[@id='LeaderBoard1_cbSeason']",
            "rookies": "//input[@id='LeaderBoard1_cbRookie']"
        }
        self.__buttons = {
            "season1": "//input[@id='LeaderBoard1_btnMSeason']",
            "season2": "//input[@id='LeaderBoard1_btnMSeason']",
            "age1": "//input[@id='LeaderBoard1_cmdAge']",
            "age2": "//input[@id='LeaderBoard1_cmdAge']"
        }

        self.__response = urlopen(
            "https://fangraphs.com/leaders.aspx"
        )
        self.__parser = etree.HTMLParser()
        self.tree = etree.parse(self.__parser, self.__response)

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
