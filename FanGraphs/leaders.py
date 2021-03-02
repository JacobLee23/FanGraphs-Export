#! python3
# FanGraphs/leaders.py

"""

"""

from urllib.request import urlopen

from lxml import etree
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class MajorLeagueLeaderboards:
    """ Parse FanGraphs >> Leaders >> Major League Leaderboards
"""
    def __init__(self):
        self.__selections = {
            "group": "//div[@id='LeaderBoard1_tsGroup']",
            "stat": "//div[@id='LeaderBoard1_tsStats']",
            "position": "//div[@id='LeaderBoard1_tsPosition']",
        }
        self.__dropdowns = {
            "league": "//div[@id='LeaderBoard1_rcbLeague']",
            "team": "//div[@id='LeaderBoard1_rcbTeam']",
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
            "team": "//div[@id='LeaderBoard1_rcbTeam_DropDown']",
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
        self.address = "https://fangraphs.com/leaders.aspx"

        self.__response = urlopen(self.address)
        self.__parser = etree.HTMLParser()
        self.tree = etree.parse(self.__response, self.__parser)

        self.__options = Options()
        self.__options.headless = True
        self.browser = webdriver.Firefox(
            options=self.__options
        )
        self.browser.get(self.address)

    class InvalidFilterQuery(Exception):

        def __init__(self, query):
            self.query = query
            self.message = f"No filter named '{self.query}' could be found"
            super().__init__(self.message)

    def list_queries(self):
        queries = {
            "selection": list(self.__selections),
            "dropdown": list(self.__dropdowns),
            "checkbox": list(self.__checkboxes)
        }
        return queries

    def list_options(self, query):
        query = query.lower()
        if query in self.__checkboxes:
            options = ["True", "False"]
        elif query in self.__dropdown_options:
            xpath = "{}//div//ul//li".format(
                self.__dropdown_options.get(query)
            )
            elems = self.tree.xpath(xpath)
            options = [e.text for e in elems]
        elif query in self.__selections:
            xpath = "{}//div//ul//li//a//span//span//span".format(
                self.__selections.get(query)
            )
            elems = self.tree.xpath(xpath)
            options = [e.text for e in elems]
        else:
            raise self.InvalidFilterQuery(query)
        return options

    def current_option(self, query):
        query = query.lower()
        if query in self.__checkboxes:
            xpath = self.__checkboxes.get(query)
            elem = self.tree.xpath(xpath)[0]
            option = "True" if elem.get("checked") == "checked" else "False"
        elif query in self.__dropdowns:
            xpath = "{}//span//input".format(
                self.__dropdowns.get(query)
            )
            elem = self.tree.xpath(xpath)[0]
            option = elem.get("value")
        elif query in self.__selections:
            xpath = "{}//div//ul//li//a[{}]//span//span//span".format(
                self.__selections.get(query),
                "@class='rtsLink rtsSelected'"
            )
            elem = self.tree.xpath(xpath)[0]
            option = elem.text
        else:
            raise self.InvalidFilterQuery(query)
        return option

    def configure(self, query, option):
        query, option = query.lower(), str(option).lower()
        while True:
            try:
                if query in self.__checkboxes:
                    self.__config_checkbox(query, option)
                elif query in self.__dropdowns:
                    self.__config_dropdown(query, option)
                elif query in self.__selections:
                    self.__config_selection(query, option)
                if query in self.__buttons:
                    self.__submit_form(query)
            except ElementClickInterceptedException:
                self.__close_ad()
                continue
            break
        self.__response = urlopen(self.browser.current_url)
        self.tree = etree.parse(self.__response, self.__parser)

    def __config_checkbox(self, query, option):
        current = self.current_option(query)
        if option == current:
            return
        elem = self.browser.find_element_by_xpath(
            self.__checkboxes.get(query)
        )
        elem.click()

    def __config_dropdown(self, query, option):
        options = [o.lower() for o in self.list_options(query)]
        index = options.index(option)
        dropdown = self.browser.find_element_by_xpath(
            "{}//span//input".format(
                self.__dropdowns.get(query)
            )
        )
        dropdown.click()
        elem = self.browser.find_elements_by_xpath(
            "{}//div//ul//li".format(
                self.__dropdown_options.get(query)
            )
        )[index]
        elem.click()

    def __config_selection(self, query, option):
        options = [o.lower() for o in self.list_options(query)]
        index = options.index(option)
        elem = self.browser.find_elements_by_xpath(
            "{}//div//ul//li".format(
                self.__selections.get(query)
            )
        )[index]
        elem.click()

    def __submit_form(self, query):
        elem = self.browser.find_element_by_xpath(
            self.__buttons.get(query)
        )
        elem.click()

    def __close_ad(self):
        elem = self.browser.find_element_by_xpath(
            "//span[@class='ezmob-footer-close']"
        )
        elem.click()

    def quit(self):
        self.browser.quit()

    def reset(self):
        self.browser.get(self.address)
        self.__response = urlopen(self.browser.current_url)
        self.tree = etree.parse(self.__response, self.__parser)


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
