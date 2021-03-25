#! python3
# tests/test_leaders.py

"""
The docstring in each class identifies the class in :py:mod:`FanGraphs.leaders` being tested.
The docstring in each test identifies the class attribute(s)/method(s) being tested.
==============================================================================
"""

import bs4
from playwright.sync_api import sync_playwright
import pytest
import requests

from FanGraphs.selectors import leaders_sel


def fetch_soup(address, waitfor=""):
    """
    Initializes the ``bs4.BeautifulSoup`` object for parsing the FanGraphs page

    :param address: The base URL address of the FanGraphs page
    :param waitfor: The CSS selector to wait for
    :return: A ``BeautifulSoup`` object for parsing the page
    :rtype: bs4.BeautifulSoup
    """
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page()
        page.goto(address, timeout=0)
        page.wait_for_selector(waitfor)
        soup = bs4.BeautifulSoup(
            page.content(), features="lxml"
        )
        browser.close()
    return soup


class TestMajorLeagueLeaderboards:
    """
    :py:class:`FanGraphs.leaders.MajorLeagueLeaderboards`
    """

    __selections = leaders_sel.mll.selections
    __dropdowns = leaders_sel.mll.dropdowns
    __dropdown_options = leaders_sel.mll.dropdown_options
    __checkboxes = leaders_sel.mll.checkboxes
    __buttons = leaders_sel.mll.buttons

    address = "https://fangraphs.com/leaders.aspx"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address)

    def test_address(self):
        """
        Class attribute ``MajorLeagueLeaderboards.address``.
        """
        res = requests.get(self.address)
        assert res.status_code == 200

    @pytest.mark.parametrize(
        "selectors",
        [__selections, __dropdown_options]
    )
    def test_list_options(self, selectors: dict):
        elem_count = {
            "group": 3, "stat": 3, "position": 13, "type": 19,
            "league": 3, "team": 31, "single_season": 151, "split": 67,
            "min_pa": 60, "season1": 151, "season2": 151, "age1": 45, "age2": 45,
            "split_teams": 2, "active_roster": 2, "hof": 2, "split_seasons": 2,
            "rookies": 2
        }
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} li")
            assert len(elems) == elem_count[query], query
            assert all([isinstance(e.getText(), str) for e in elems]), query

    def test_current_option_selections(self):
        """
        Instance method ``MajorLeagueLeaderboards.current_option``.

        Uses the selectors in:

        - ``MajorLeagueLeaderboards.__selections``
        """
        elem_text = {
            "group": "Player Stats", "stat": "Batting", "position": "All",
            "type": "Dashboard"
        }
        for query, sel in self.__selections.items():
            elem = self.soup.select(f"{sel} .rtsLink.rtsSelected")
            assert len(elem) == 1, query
            assert isinstance(elem[0].getText(), str), query
            assert elem[0].getText() == elem_text[query]

    def test_current_option_dropdowns(self):
        """
        Instance method ``MajorLeagueLeaderboards.current_option``.

        Uses the selectors in:

        - ``MajorLeagueLeaderboards.__dropdowns``
        """
        elem_value = {
            "league": "All Leagues", "team": "All Teams", "single_season": "2020",
            "split": "Full Season", "min_pa": "Qualified", "season1": "2020",
            "season2": "2020", "age1": "14", "age2": "58"
        }
        for query, sel in self.__dropdowns.items():
            elem = self.soup.select(sel)[0]
            assert elem.get("value") is not None, query
            assert elem_value[query] == elem.get("value")

    @pytest.mark.parametrize(
        "selectors",
        [__selections, __dropdowns, __dropdown_options,
         __checkboxes, __buttons]
    )
    def test_configure(self, selectors: dict):
        """
        Private instance method ``MajorLeagueLeaderboards.__configure_selection``.
        Private instance method ``MajorLeagueLeaderboards.__configure_dropdown``.
        Private instance method ``MajorLeagueLeaderboards.__configure_checkbox``.
        Private instance method ``MajorLeagueLeaderboards.__click_button``.

        :param selectors: CSS Selectors
        """
        for query, sel in selectors.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_expand_sublevel(self):
        """
        Statement in private instance method ``MajorLeagueLeaderboards.__configure_selection``.
        """
        elems = self.soup.select("#LeaderBoard1_tsType a[href='#']")
        assert len(elems) == 1

    def test_export(self):
        """
        Instance method ``MajorLeagueLeaderboards.export``.
        """
        elems = self.soup.select("#LeaderBoard1_cmdCSV")
        assert len(elems) == 1


class TestSplitsLeaderboards:
    """
    :py:class:`FanGraphs.leaders.SplitsLeaderboards`.
    """

    __selections = leaders_sel.splits.selections
    __dropdowns = leaders_sel.splits.dropdowns
    __splits = leaders_sel.splits.splits
    __quick_splits = leaders_sel.splits.quick_splits
    __switches = leaders_sel.splits.switches

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address, leaders_sel.splits.waitfor)

    def test_address(self):
        """
        Class attribute ``SplitsLeaderboards.address``.
        """
        res = requests.get(self.address)
        assert res.status_code == 200

    def test_list_options_selections(self):
        """
        Instance method ``SplitsLeaderboards.list_options``.

        Uses the selectors in:

        - ``SplitsLeaderboards.__selections``
        """
        elem_count = {
            "group": 4, "stat": 2, "type": 3
        }
        for query, sel_list in self.__selections.items():
            elems = [self.soup.select(s)[0] for s in sel_list]
            assert len(elems) == elem_count[query]
            assert all([e.getText() for e in elems])

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns, __splits]
    )
    def test_list_options(self, selectors: dict):
        """
        Instance method ``SplitsLeaderboards.list_options``.

        Uses the selectors in:

        - ``SplitsLeaderboards.__dropdowns``
        - ``SplitsLeaderboards.__splits``

        :param selectors: CSS selectors
        """
        elem_count = {
            "time_filter": 10, "preset_range": 12, "groupby": 5,
            "handedness": 4, "home_away": 2, "batted_ball": 15,
            "situation": 7, "count": 11, "batting_order": 9, "position": 12,
            "inning": 10, "leverage": 3, "shifts": 3, "team": 32,
            "opponent": 32,
        }
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} li")
            assert len(elems) == elem_count[query]

    def test_current_option_selections(self):
        """
        Instance method ``SplitsLeaderboards.current_option``.

        Uses the selectors in:

        - ``SplitsLeaderboards.__selections``
        """
        elem_text = {
            "group": "Player", "stat": "Batting", "type": "Standard"
        }
        for query, sel_list in self.__selections.items():
            elems = []
            for sel in sel_list:
                elem = self.soup.select(sel)[0]
                assert elem.get("class") is not None
                elems.append(elem)
            active = ["isActive" in e.get("class") for e in elems]
            assert active.count(True) == 1, query
            text = [e.getText() for e in elems]
            assert elem_text[query] in text

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns, __splits, __switches]
    )
    def test_current_option(self, selectors: dict):
        """
        Instance method ``SplitsLeaderboards.current_option``.

        Uses the selectors in:

        - ``SplitsLeaderboards.__dropdowns``
        - ``SplitsLeaderboards.__splits``
        - ``SplitsLeaderboards.__switches``

        :param selectors: CSS selectors
        """
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} li")
            for elem in elems:
                assert elem.get("class") is not None, query

    def test_configure_selection(self):
        """
        Private instance method ``SplitsLeaderboards.__configure_selection``.
        """
        for query, sel_list in self.__selections.items():
            for sel in sel_list:
                elems = self.soup.select(sel)
                assert len(elems) == 1, query

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns, __splits, __switches]
    )
    def test_configure(self, selectors: dict):
        """
        Private instance method ``SplitsLeaderboards.__configure_dropdown``.
        Private instance method ``SplitsLeaderboards.__configure_split``.
        Private instance method ``SplitsLeaderboards.__configure_switch``.

        :param selectors: CSS Selectors
        """
        for query, sel in selectors.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_update(self):
        """
        Instance method ``SplitsLeaderboards.update``.
        """
        elems = self.soup.select("#button-update")
        assert len(elems) == 0

    def test_list_filter_groups(self):
        """
        Instance method ``SplitsLeaderboards.list_filter_groups``.
        """
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        assert len(elems) == 4
        options = ["Quick Splits", "Splits", "Filters", "Show All"]
        assert [e.getText() for e in elems] == options

    def test_configure_filter_group(self):
        """
        Instance method ``SplitsLeaderboards.configure_filter_group``.
        """
        groups = ["Quick Splits", "Splits", "Filters", "Show All"]
        elems = self.soup.select(".fgBin.splits-bin-controller div")
        assert len(elems) == 4
        assert [e.getText() for e in elems] == groups

    def test_reset_filters(self):
        """
        Instance method ``SplitsLeaderboards.reset_filters``.
        """
        elems = self.soup.select("#stack-buttons .fgButton.small:nth-last-child(1)")
        assert len(elems) == 1

    def test_configure_quick_split(self):
        """
        Instance method ``SplitsLeaderboards.configure_quick_split``.
        """
        for qsplit, sel in self.__quick_splits.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, qsplit

    def test_export(self):
        """
        Instance method ``SplitsLeaderboards.export``.
        """
        elems = self.soup.select(".data-export")
        assert len(elems) == 1


class TestSeasonStatGrid:
    """
    :py:class:`FanGraphs.leaders.SeasonStatGrid`.
    """
    __selections = leaders_sel.ssg.selections
    __dropdowns = leaders_sel.ssg.dropdowns

    address = "https://fangraphs.com/leaders/season-stat-grid"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address, leaders_sel.ssg.waitfor)

    def test_address(self):
        """
        Class attribute ``SeasonStatGrid.address``
        """
        res = requests.get(self.address)
        assert res.status_code == 200

    def test_list_options_selections(self):
        """
        Instance method ``SeasonStatGrid.list_options``.

        Uses the following class attributes:

        - ``SeasonStatGrid.__selections``
        """
        elem_count = {
            "stat": 2, "group": 3, "type": 3
        }
        for query, sel_list in self.__selections.items():
            elems = [self.soup.select(s)[0] for s in sel_list]
            assert len(elems) == elem_count[query]
            assert all([e.getText() for e in elems])

    def test_list_options_dropdowns(self):
        """
        Instance method ``SeasonStatGrid.list_options``.

        Uses the following class attributes:

        - ``SeasonStatGrid.__dropdowns``
        """
        elem_count = {
            "start_season": 71, "end_season": 71, "popular": 6,
            "standard": 20, "advanced": 17, "statcast": 8, "batted_ball": 24,
            "win_probability": 10, "pitch_type": 25, "plate_discipline": 25,
            "value": 11
        }
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(f"{sel} li")
            assert len(elems) == elem_count[query], query
            assert all([e.getText() for e in elems])

    def test_current_option_selections(self):
        """
        Instance method ``SeasonStatGrid.current_option``.

        Tests the following class attributes:

        - ``SeasonStatGrid.__selections``
        """
        selector = "div[class='fgButton button-green active isActive']"
        elems = self.soup.select(selector)
        assert len(elems) == 2

    def test_current_options_dropdowns(self):
        """
        Instance method ``SeasonStatGrid.current_option``.

        Uses the following class attributes:

        - ``SeasonStatGrid.__dropdowns``
        """
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(
                f"{sel} li[class$='highlight-selection']"
            )
            if query in ["start_season", "end_season", "popular", "value"]:
                assert len(elems) == 1, query
                assert elems[0].getText() is not None
            else:
                assert len(elems) == 0, query

    def test_configure_selection(self):
        """
        Private instance method ``SeasonStatGrid.__configure_selection``.
        """
        for query, sel_list in self.__selections.items():
            for sel in sel_list:
                elems = self.soup.select(sel)
                assert len(elems) == 1, query

    def test_configure_dropdown(self):
        """
        Private instance method ``SeasonStatGrid.__configure_dropdown``.
        """
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_export(self):
        total_pages = self.soup.select(
            ".table-page-control:nth-last-child(1) > .table-control-total"
        )
        assert len(total_pages) == 1
        assert total_pages[0].getText().isdecimal()
        arrow = self.soup.select(
            ".table-page-control:nth-last-child(1) > .next"
        )
        assert len(arrow) == 1
        assert arrow[0].getText() == "chevron_right"


class TestGameSpanLeaderboards:
    """
    :py:class:`GameSpanLeaderboards`.
    """
    __selections = leaders_sel.gsl.selections
    __dropdowns = leaders_sel.gsl.dropdowns

    address = "https://www.fangraphs.com/leaders/special/60-game-span"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address, leaders_sel.gsl.waitfor)

    def test_address(self):
        """
        Class attribute ``GameSpanLeaderboards.address``.
        """
        res = requests.get(self.address)
        assert res.status_code == 200

    def test_list_options_selections(self):
        """
        Instance method ``GameSpanLeaderboards.list_options``.

        Uses the following class attributes:

        - ``GameSpanLeaderboards.__selections``
        """
        elem_count = {
            "stat": 2, "type": 3
        }
        for query, sel_list in self.__selections.items():
            elems = [self.soup.select(s)[0] for s in sel_list]
            assert len(elems) == elem_count[query], query
            assert all([e.getText() for e in elems]), query

    def test_list_options_dropdowns(self):
        """
        Instance method ``GameSpanLeaderboards.list_options``.

        Uses the following class attributes:

        - ``GameSpanLeaderboards.__dropdowns``
        """
        elem_count = {
            "min_pa": 9, "single_season": 46, "season1": 46, "season2": 46,
            "determine": 11
        }
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(f"{sel} > div > a")
            assert len(elems) == elem_count[query], query
            assert all([e.getText() for e in elems]), query

    def test_current_option_selections(self):
        """
        Instance method ``GameSpanLeaderboards.current_option``.

        Uses the following class attributes:

        - ``GameSpanLeaderboards.__selections``
        """
        elem_text = {
            "stat": "Batters", "type": "Best 60-Game Span"
        }
        for query, sel_list in self.__selections.items():
            elems = []
            for sel in sel_list:
                elem = self.soup.select(sel)[0]
                assert elem.get("class") is not None, query
                elems.append(elem)
            active = ["active" in e.get("class") for e in elems]
            assert active.count(True) == 1, query
            text = [e.getText() for e in elems]
            assert elem_text[query] in text, query

    def test_current_option_dropdown(self):
        """
        Instance method ``GameSpanLeaderboards.current_option``.

        Uses the following class attributes:

        - ``GameSpanLeaderboards.__dropdowns``
        """
        elem_text = {
            "min_pa": "Qualified", "single_season": "Select",
            "season1": "Select", "season2": "Select",
            "determine": "WAR"
        }
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(f"{sel} > div > span")
            assert len(elems) == 1, query
            text = elems[0].getText()
            assert text == elem_text[query], query

    def test_configure_selections(self):
        """
        Private instance method ``GameSpanLeaderboards.__configure_selection``.
        """
        for query, sel_list in self.__selections.items():
            for sel in sel_list:
                elems = self.soup.select(sel)
                assert len(elems) == 1, query

    def test_configure_dropdown(self):
        """
        Private instance method ``GameSpanLeaderboards.__configure_dropdown``.
        """
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_export(self):
        """
        Instance method ``GameSpanLeaderboards.export``.
        """
        elems = self.soup.select(".data-export")
        assert len(elems) == 1


class TestInternationalLeaderboards:
    """
    :py:class:`FanGraphs.leaders.InternationalLeaderboards`
    """
    __selections = leaders_sel.intl.selections
    __dropdowns = leaders_sel.intl.dropdowns
    __checkboxes = leaders_sel.intl.checkboxes
    address = "https://www.fangraphs.com/leaders/international"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address, waitfor=leaders_sel.intl.waitfor)

    def test_address(self):
        """
        Class attribute ``InternationalLeaderboards.address``.
        """
        res = requests.get(self.address)
        assert res.status_code == 200

    def test_list_options_selections(self):
        """
        Instance method ``InternationalLeaderboards.list_options``.

        Uses the following class attributes:

        - ``InternationalLeaderboards.__selections``
        """
        elem_count = {
            "stat": 2, "type": 2
        }
        for query, sel_list in self.__selections.items():
            elems = [self.soup.select(s)[0] for s in sel_list]
            assert len(elems) == elem_count[query], query
            assert all([e.getText() for e in elems]), query

    def test_list_options_dropdowns(self):
        """
        Instance method ``InternationalLeaderboards.list_options``.

        Uses the following class attributes:

        - ``InternationalLeaderboards.__dropdowns``
        """
        elem_count = {
            "position": 11, "min": 42, "single_season": 19, "season1": 19, "season2": 19,
            "league": 1, "team": 11
        }
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(f"{sel} > div > a")
            assert len(elems) == elem_count[query], query
            assert all([e.getText() for e in elems]), query

    def test_current_option_selections(self):
        """
        Instance method ``InternationalLeaderboards.current_option``.

        Uses the following class attributes:

        - ``InternationalLeaderboards.__selections``
        """
        elem_text = {
            "stat": "Batters", "type": "Standard"
        }
        for query, sel_list in self.__selections.items():
            elems = []
            for sel in sel_list:
                elem = self.soup.select(sel)[0]
                assert elem.get("class") is not None, query
                elems.append(elem)
            active = ["active" in e.get("class") for e in elems]
            assert active.count(True) == 1, query
            text = [e.getText() for e in elems]
            assert elem_text[query] in text, query

    def test_current_option_dropdown(self):
        """
        Instance method ``InternationalLeaderboards.current_option``.

        Uses the following class attributes:

        - ``InternationalLeaderboards.__dropdowns``
        """
        elem_text = {
            "position": "All", "min": "Qualified", "single_season": "2020",
            "season1": "2020", "season2": "2020", "league": "KBO",
            "team": "Select"
        }
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(f"{sel} > div > span")
            assert len(elems) == 1, query
            text = elems[0].getText()
            assert text == elem_text[query], query

    def test_configure_selections(self):
        """
        Private instance method ``InternationalLeaderboards.__configure_selection``.
        """
        for query, sel_list in self.__selections.items():
            for sel in sel_list:
                elems = self.soup.select(sel)
                assert len(elems) == 1, query

    def test_configure_dropdown(self):
        """
        Private instance method ``InternationalLeaderboards.__configure_dropdown``.
        """
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_export(self):
        """
        Instance method ``InternationalLeaderboards.export``.
        """
        elems = self.soup.select(".data-export")
        assert len(elems) == 1


class TestWARLeaderboards:
    """
    :py:class:`FanGraphs.leaders.WARLeaderboards`
    """
    __dropdowns = leaders_sel.war.dropdowns
    __dropdown_options = leaders_sel.war.dropdown_options

    address = "https://fangraphs.com/warleaders.aspx"

    @classmethod
    def setup_class(cls):
        cls.soup = fetch_soup(cls.address, waitfor=leaders_sel.war.waitfor)

    @pytest.mark.parametrize(
        "selectors",
        [__dropdown_options]
    )
    def test_list_options(self, selectors: dict):
        """
        Instance method ``WARLeaderboards.list_options``

        :param selectors: The CSS selectors
        """
        elem_count = {
            "season": 151, "team": 33, "type": 3
        }
        for query, sel in selectors.items():
            elems = self.soup.select(f"{sel} > ul > li")
            assert len(elems) == elem_count[query], query

    @pytest.mark.parametrize(
        "selectors",
        [__dropdowns]
    )
    def test_current_option(self, selectors: dict):
        elem_text = {
            "season": "2020", "team": "All Teams", "type": "WAR (FIP Based)"
        }
        for query, sel in selectors.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query
            assert elems[0].get("value") is not None, query
            assert elems[0].get("value") == elem_text[query], query

    def test_configure_dropdown(self):
        for query, sel in self.__dropdowns.items():
            elems = self.soup.select(sel)
            assert len(elems) == 1, query

    def test_export(self):
        elems = self.soup.select("#WARBoard1_cmdCSV")
        assert len(elems) == 1
