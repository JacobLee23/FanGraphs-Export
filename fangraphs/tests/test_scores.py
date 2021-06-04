#! python3
# fangraphs/tests/test_scores.py

"""
Unit tests for :py:mod:`fangraphs.scores`.
"""

import datetime
import re
from urllib.request import urlopen

from playwright.sync_api import sync_playwright
import pytest

from fangraphs.tests import BaseTests


@pytest.fixture(scope="module")
def page(request):
    """

    :return: A Playwright ``Page`` objects
    :rtype: playwright.sync_api._generated.Page
    """
    with sync_playwright() as play:
        try:
            browser = play.chromium.launch()
            webpage = browser.new_page()
            webpage.goto(
                request.getfixturevalue(request.param),
                timeout=0.0
            )
            yield webpage
        finally:
            browser.close()


@pytest.fixture(scope="module")
def live_page():
    return TestLive.address


@pytest.fixture(scope="module")
def liveleaderboards_page():
    return TestLiveLeaderboards.address


@pytest.fixture(scope="module")
def scoreboard_page():
    return TestScoreboard.address


@pytest.fixture(scope="module")
def gamegraphs_page():
    return TestGameGraphs.address


def _test_scrape_sotg(page):
    """
    :py:func:`fangraphs.scores._scrape_sotg`

    :param page: A Playwright ``Page`` object
    :type page: playwright.sync_api._generated.Page
    """
    sotg_regex = re.compile(r"(.*) \((.*) / (.*)\)")

    assert len(
        page.query_selector_all(
            "#WinsGame1_ThreeStars1_ajaxPanel > #pan1"
        )
    ) == 1
    sotg_table = page.query_selector(
        "#WinsGame1_ThreeStars1_ajaxPanel > #pan1"
    )

    assert len(
        sotg_table.query_selector_all(
            "tr > td:nth-child(1)"
        )
    ) == 4, sotg_table.inner_html()
    sotgs = sotg_table.query_selector_all("tr > td:nth-child(1)")[1:]

    stars_of_the_game = [e.text_content().strip() for e in sotgs]
    assert all(stars_of_the_game)

    assert all(
        sotg_regex.search(s) is not None for s in stars_of_the_game if s != "No Votes Yet"
    )


def _test_scrape_headers(table):
    """
    :py:func:`fangraphs.scores._scrape_headers`

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    """
    elems = table.query_selector_all("thead > tr > th")
    if elems[0].text_content() == "Pitcher":
        assert len(elems) == 9, table.inner_html()
    elif elems[0].text_content() == "Batter":
        assert len(elems) == 10, table.inner_html()
    else:
        pytest.fail(table.inner_html())

    headers = [e.text_content() for e in elems]
    assert all(headers), headers


def _test_scrape_table(table):
    """
    :py:func:`fangraphs.scores._scrape_table`

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    """
    _test_scrape_headers(table)

    href_regex = re.compile(r"statss.aspx\?playerid=(.*)&position=.*")

    rows = table.query_selector_all("tbody > tr")[:-1]
    assert rows, table.inner_html()

    for row in rows:
        elems = row.query_selector_all("td")
        items = [e.text_content() for e in elems]
        assert all(items)

        href = elems[0].query_selector("a").get_attribute("href")
        assert href_regex.search(href), href

    total = table.query_selector("tbody > tr:nth-last-child(1)")
    assert total.query_selector("td:nth-child(1)").text_content() == "Total"


def _test_scrape_game(game):
    """
    :py:func:`fangraphs.scores._scrape_game`

    :param game:
    :type game: playwright.sync_api._generated.ElementHandle
    """
    a_elems = game.query_selector_all("xpath=./a")
    assert len(a_elems) == 3, game.inner_html()

    a_text = [e.text_content() for e in a_elems]
    assert set(a_text) == {"Box Score", "Win Probability", "Play Log"}

    hyperlinks = [
        f"https://fangraphs.com/{e.get_attribute('href').replace(' ', '%20')}"
        for e in a_elems
    ]
    for link in hyperlinks:
        assert urlopen(link).getcode() == 200, link

    assert len(
        game.query_selector_all(
            "div[id*='graph']:nth-child(1) > div > svg > text.highcharts-title > tspan"
        )
    ) == 1, game.inner_html()
    game_info = game.query_selector(
        "div[id*='graph']:nth-child(1) > div > svg > text.highcharts-title > tspan"
    )

    game_info_regex = re.compile(r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)")
    assert game_info_regex.search(game_info.text_content()), game_info.text_content()

    date, away_team, away_score, home_team, home_score = game_info_regex.search(
        game_info.text_content()
    ).groups()

    date_dt = datetime.datetime.strptime(date, "%m/%d/%Y")
    assert date_dt


def _test_scrape_preview(preview):
    """
    :py:func:`fangraphs.scores._scrape_preview`

    :param preview:
    :type preview: playwright.sync_api._generated.ElementHandle
    """
    assert len(
        preview.query_selector_all("b > a")
    ) == 2, preview.inner_html()
    away_team, home_team = [
        e.text_content() for e in preview.query_selector_all("b > a")
    ]
    assert all((away_team, home_team))

    time_regex = re.compile(r"\d{1,2}:\d{1,2} ET")
    time_dt = datetime.datetime.strptime(
        time_regex.search(preview.text_content()).group(),
        "%H:%M ET"
    )
    assert time_dt

    assert len(
        preview.query_selector_all(
            "center > table.lineup tr > td"
        )
    ) == 4
    away_sp, home_sp, away_lineup, home_lineup = [
        e for e in preview.query_selector_all(
            "center > table.lineup tr > td"
        )
    ]
    away_sp, home_sp = (
        away_sp.text_content().split(": "),
        home_sp.text_content().split(": ")
    )
    assert away_sp[0] == "SP" and home_sp[0] == "SP"

    pplayer_regex = re.compile(r"(\d+)\. (.*?) \((.*?)\)")
    if pplayer_regex.search(home_lineup.text_content()):
        assert len(
            pplayer_regex.findall(home_lineup.text_content())
        ) == 9, home_lineup
    if pplayer_regex.search(away_lineup.text_content()):
        assert len(
            pplayer_regex.findall(away_lineup.text_content())
        ) == 9, away_lineup


class TestLive(BaseTests):
    """
    :py:class:`fangraphs.scores.Live`
    """
    address = "https://www.fangraphs.com/livescoreboard.aspx"

    @pytest.mark.parametrize(
        "page", ["live_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.scores.Live.export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        :rtype: None
        """
        assert len(
            page.query_selector_all(
                "#LiveBoard1_LiveBoard1_litGamesPanel > table:nth-last-child(1) > tbody"
            )
        ) == 1
        table_body = page.query_selector(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table:nth-last-child(1) > tbody"
        )
        matches = table_body.query_selector_all(
            "td[style*='border-bottom:1px dotted black;']"
        )
        assert matches

        for match in matches:
            if (
                    len(match.query_selector_all("xpath=./div")) == 2
                    and len(match.query_selector_all("xpath=./a")) == 3
            ):
                _test_scrape_game(match)
            elif (
                    len(match.query_selector_all("xpath=./b")) == 2
                    and len(match.query_selector_all("xpath=./center")) == 1
            ):
                _test_scrape_preview(match)
            else:
                raise AssertionError(
                    (len(match.query_selector_all("xpath=./div")),
                     len(match.query_selector_all("xpath=./a"))),
                    (len(match.query_selector_all("xpath=./b")),
                     len(match.query_selector_all("xpath=./center")))
                )


class TestLiveLeaderboards(BaseTests):
    """
    :py:class:`fangraphs.scores.LiveLeaderboards`
    """
    address = "https://fangraphs.com/scores/live-leaderboards"

    @staticmethod
    def _test_scrape_table_headers(table):
        """
        :py:meth:`fangraphs.scores.LiveLeaderboards._scrape_table_headers`

        :param table: The table element
        :type table: playwright.sync_api._generated.ElementHandle
        """
        header_elems = table.query_selector_all("thead > tr > th")[1:]
        assert len(header_elems) == 16, table.inner_html()

        headers = [e.text_content() for e in header_elems]
        assert all(headers), headers

    @staticmethod
    def _test_scrape_table_rows(table):
        """
        :py:meth:`fangraphs.scores.LiveLeaderboards._scrape_table_rows`

        :param table: The table element
        :type table: playwright.sync_api._generated.ElementHandle
        """
        rows = table.query_selector_all("tbody > tr")
        assert rows, table.inner_html()

        href_regex = re.compile(r"//www.fangraphs.com/statss.aspx\?playerid=(.*)")
        opp_regex = re.compile(r"(@)?(.*)(\d+-\d+ \((F|Top|Bottom) \d+\))")

        for i, row in enumerate(rows):
            elems = row.query_selector_all("td")[1:]
            assert elems, row.inner_html()

            data = [e.text_content() for e in elems]
            assert data, row.inner_html()

            href = elems[0].query_selector("a").get_attribute("href")
            assert href_regex.search(href), href

            assert opp_regex.search(data[2]), data[2]

    @pytest.mark.parametrize(
        "page", ["liveleaderboards_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.scores.LiveLeaderboards.export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        """
        assert len(
            page.query_selector_all(
                ".table-fixed > table"
            )
        ) == 1
        table = page.query_selector(".table-fixed > table")
        self._test_scrape_table_headers(table)
        self._test_scrape_table_rows(table)


class TestScoreboard(BaseTests):
    """
    :py:class:`fangraphs.scores.Scoreboard`
    """
    address = "https://fangraphs.com/scoreboard.aspx"

    @pytest.mark.parametrize(
        "page", ["scoreboard_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.scores.Scoreboard.export`

        :param page: A Playwright ``Page`` objects
        :type page: playwright.sync_api._generated.Page
        """
        assert len(
            page.query_selector_all(
                "#content > table > tbody > tr > td > table:nth-last-child(1) > tbody"
            )
        ) == 1
        table_body = page.query_selector(
            "#content > table > tbody > tr > td > table:nth-last-child(1) > tbody"
        )
        matches = table_body.query_selector_all(
            "td[style*='border-bottom:1px dotted black;']"
        )
        assert matches

        for match in matches:
            assert (
                    len(match.query_selector_all("xpath=./div")) == 2
                    and len(match.query_selector_all("xpath=./a")) == 3
            ), match.inner_html()
            _test_scrape_game(match)


class TestGameGraphs(BaseTests):
    """
    :py:class:`fangraphs.scores.GameGraphs`
    """
    address = "https://fangraphs.com/wins.aspx"

    @pytest.mark.parametrize(
        "page", ["gamegraphs_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.scores.GameGraphs.export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        """
        _test_scrape_sotg(page)

        tables = page.query_selector_all(
            "div.RadGrid.RadGrid_FanGraphs > table.rgMasterTable"
        )
        assert len(tables) == 4

        for table in tables:
            _test_scrape_table(table)
