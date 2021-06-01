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


def _test_scrape_game(game):
    """
    :py:func:`fangraphs.scores._scrape_game`

    :param game:
    :type game: playwright.sync_api._generated.ElementHandle
    :rtype: None
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
    :rtype: None
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
                "#LiveBoard1_LiveBoard1_litGamesPanel > table > tbody"
            )
        ) == 1
        matches = page.query_selector_all(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table > tbody > tr > td[style*='border-bottom:1px dotted black;']"
        )

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
