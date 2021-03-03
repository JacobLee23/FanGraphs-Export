#! python3
# FanGraphs/leaders.py

"""

"""

import datetime
import os
from urllib.request import urlopen

from lxml import etree
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class MajorLeagueLeaderboards:
    """
    Parses the FanGraphs Major League Leaderboards page.
    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`
    """

    def __init__(self):
        """
        .. py:attribute:: address
            The base URL address of the Major League Leaderboards page

            :type: str
            :value: https://fangraphs.com/leaders.aspx

        .. py:attribute:: tree
            The ``lxml`` element tree for parsing the webpage HTML.

            :type: lxml.etree._ElementTree

        .. py:attribute:: browser
            The ``selenium`` automated Firefox browser for navigating webpage.

            :type: selenium.webdriver.firefox.webdriver.WebDriver

        """
        self.__selections = {
            "group": "LeaderBoard1_tsGroup",
            "stat": "LeaderBoard1_tsStats",
            "position": "LeaderBoard1_tsPosition",
            "type": "LeaderBoard1_tsType"
        }
        self.__dropdowns = {
            "league": "LeaderBoard1_rcbLeague_Input",
            "team": "LeaderBoard1_rcbTeam_Input",
            "single_season": "LeaderBoard1_rcbSeason_Input",
            "split": "LeaderBoard1_rcbMonth_Input",
            "min_pa": "LeaderBoard1_rcbMin_Input",
            "season1": "LeaderBoard1_rcbSeason1_Input",
            "season2": "LeaderBoard1_rcbSeason2_Input",
            "age1": "LeaderBoard1_rcbAge1_Input",
            "age2": "LeaderBoard1_rcbAge2_Input"
        }
        self.__dropdown_options = {
            "league": "LeaderBoard1_rcbLeague_DropDown",
            "team": "LeaderBoard1_rcbTeam_DropDown",
            "single_season": "LeaderBoard1_rcbSeason_DropDown",
            "split": "LeaderBoard1_rcbMonth_DropDown",
            "min_pa": "LeaderBoard1_rcbMin_DropDown",
            "season1": "LeaderBoard1_rcbSeason1_DropDown",
            "season2": "LeaderBoard1_rcbSeason2_DropDown",
            "age1": "LeaderBoard1_rcbAge1_DropDown",
            "age2": "LeaderBoard1_rcbAge2_DropDown"
        }
        self.__checkboxes = {
            "split_teams": "LeaderBoard1_cbTeams",
            "active_roster": "LeaderBoard1_cbActive",
            "hof": "LeaderBoard1_cbHOF",
            "split_seasons": "LeaderBoard1_cbSeason",
            "rookies": "LeaderBoard1_cbRookie"
        }
        self.__buttons = {
            "season1": "LeaderBoard1_btnMSeason",
            "season2": "LeaderBoard1_btnMSeason",
            "age1": "LeaderBoard1_cmdAge",
            "age2": "LeaderBoard1_cmdAge"
        }
        self.address = "https://fangraphs.com/leaders.aspx"

        response = urlopen(self.address)
        parser = etree.HTMLParser()
        self.tree = etree.parse(response, parser)

        options = Options()
        options.headless = True
        os.makedirs("dist", exist_ok=True)
        preferences = {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": os.path.abspath("dist"),
            "browser.helperApps.neverAsk.saveToDisk": "text/csv"
        }
        for pref in preferences:
            options.set_preference(pref, preferences[pref])
        self.browser = webdriver.Firefox(
            options=options
        )
        self.browser.get(self.address)

    class InvalidFilterQuery(Exception):

        def __init__(self, query):
            """
            Raised when an invalid filter query is used.

            :param query: The filter query used
            """
            self.query = query
            self.message = f"No filter named '{self.query}' could be found"
            super().__init__(self.message)

    def list_queries(self):
        """
        Lists the possible filter queries which can be used to modify search results.

        :return: Filter queries which can be used to modify search results
        :type: list
        """
        queries = []
        queries.extend(list(self.__selections))
        queries.extend(list(self.__dropdowns))
        queries.extend(list(self.__checkboxes))
        return queries

    def list_options(self, query):
        """
        Lists the possible options which the filter query can be configured to.

        :param query:
        :return: Options which the filter query can be configured to
        :rtype: list
        :raises MajorLeagueLeaderboards.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__checkboxes:
            options = ["True", "False"]
        elif query in self.__dropdown_options:
            xpath = "//div[@id='{}']//div//ul//li".format(
                self.__dropdown_options.get(query)
            )
            elems = self.tree.xpath(xpath)
            options = [e.text for e in elems]
        elif query in self.__selections:
            xpath = "//div[@id='{}']//div//ul//li//a//span//span//span".format(
                self.__selections.get(query)
            )
            elems = self.tree.xpath(xpath)
            options = [e.text for e in elems]
        else:
            raise self.InvalidFilterQuery(query)
        return options

    def current_option(self, query):
        """
        Retrieves the option which the filter query is currently set to.

        :param query: The filter query being retrieved of its current option
        :return: The option which the filter query is currently set to
        :rtype: str
        :raises MajorLeagueLeaderboards.InvalidFilterQuery: Argument ``query`` is invalid
        """
        query = query.lower()
        if query in self.__checkboxes:
            xpath = "//input[@id='{}']".format(
                self.__checkboxes.get(query)
            )
            elem = self.tree.xpath(xpath)[0]
            option = "True" if elem.get("checked") == "checked" else "False"
        elif query in self.__dropdowns:
            xpath = "//input[@id='{}']".format(
                self.__dropdowns.get(query)
            )
            elem = self.tree.xpath(xpath)[0]
            option = elem.get("value")
        elif query in self.__selections:
            xpath = "//div[@id='{}']//div//ul//li//a[@class='{}']//span//span//span".format(
                self.__selections.get(query),
                "rtsLink rtsSelected"
            )
            elem = self.tree.xpath(xpath)[0]
            option = elem.text
        else:
            raise self.InvalidFilterQuery(query)
        return option

    def configure(self, query, option):
        """
        Sets a filter query to a specified option.

        :param query: The filter query to be configured
        :param option: The option to set the filter query to
        """
        query, option = query.lower(), str(option).lower()
        if query not in self.list_queries():
            raise self.InvalidFilterQuery(query)
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
            except exceptions.ElementClickInterceptedException:
                self.__close_ad()
                continue
            break
        response = urlopen(self.browser.current_url)
        parser = etree.HTMLParser()
        self.tree = etree.parse(response, parser)

    def __config_checkbox(self, query, option):
        """
        Sets a checkbox-class filter query to an option

        :param query: The checkbox-class filter query to be configured
        :param option: The option to set the filter query to
        """
        current = self.current_option(query).lower()
        if option == current:
            return
        elem = self.browser.find_element_by_xpath(
            self.__checkboxes.get(query)
        )
        elem.click()

    def __config_dropdown(self, query, option):
        """
        Sets a dropdown-class filter query to an option

        :param query: The dropdown-class filter query to be configured
        :param option: The option to set the filter query to
        """
        options = [o.lower() for o in self.list_options(query)]
        index = options.index(option)
        dropdown = self.browser.find_element_by_id(
            self.__dropdowns.get(query)
        )
        dropdown.click()
        elem = self.browser.find_elements_by_css_selector(
            "div[id='{}'] div ul li".format(
                self.__dropdown_options.get(query)
            )
        )[index]
        elem.click()

    def __config_selection(self, query, option):
        """
        Sets a selection-class filter query to an option

        :param query: The selection-class filter query to be configured
        :param option: The option to set the filter query to
        """
        def open_pitch_type_sublevel():
            pitch_type_elem = self.browser.find_element_by_css_selector(
                "div[id='LeaderBoard1_tsType'] div ul li a[href='#']"
            )
            pitch_type_elem.click()
        options = [o.lower() for o in self.list_options(query)]
        index = options.index(option)
        elem = self.browser.find_elements_by_css_selector(
            "div[id='{}'] div ul li".format(
                self.__selections.get(query)
            )
        )[index]
        try:
            elem.click()
        except exceptions.ElementNotInteractableException:
            open_pitch_type_sublevel()
            elem.click()

    def __submit_form(self, query):
        """
        Clicks the button element which submits the search query.

        :param query: The filter query which has an attached form submission button
        """
        elem = self.browser.find_element_by_id(
            self.__buttons.get(query)
        )
        elem.click()

    def __close_popup(self):
        pass

    def __close_ad(self):
        """
        Closes the ad which may interfere with clicking other page elements.
        """
        elem = self.browser.find_element_by_class_name(
            "ezmob-footer-close"
        )
        elem.click()

    def quit(self):
        """
        Calls the ``quit()`` method of :py:attr:`browser`.
        """
        self.browser.quit()

    def reset(self):
        """
        Calls the ``get()`` method of :py:attr:`browser`, passing :py:attr:`address`.
        """
        self.browser.get(self.address)
        response = urlopen(self.browser.current_url)
        parser = etree.HTMLParser()
        self.tree = etree.parse(response, parser)

    def export(self, name=""):
        """
        Exports the current leaderboard as a CSV file.
        The file will be saved to *./dist*.
        By default, the name of the file is **FanGraphs Leaderboard.csv**.
        If ``name`` is not specified, the file will be the formatted ``datetime.datetime.now()``.

        :param name: The filename to rename the saved file to
        """
        if not name or os.path.splitext(name)[1] != ".csv":
            name = "{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        while True:
            try:
                WebDriverWait(self.browser, 20).until(
                    expected_conditions.element_to_be_clickable(
                        (By.ID, "LeaderBoard1_cmdCSV")
                    )
                ).click()
                break
            except exceptions.ElementClickInterceptedException:
                self.__close_ad()
        os.rename(
            os.path.join("dist", "FanGraphs Leaderboard.csv"),
            os.path.join("dist", name)
        )


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
