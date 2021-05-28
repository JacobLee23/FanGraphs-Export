#! python3
# fangraphs/tests/test_scores.py

"""
Unit tests for :py:mod:`fangraphs.scores`.
"""

import datetime
import re

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
            browser = play.chromium.launch(headless=False)
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


def _test_scrape_leverage_index(leverage_index):
    """
    :py:func:`fangraphs.scores._scrape_charts`

    :param leverage_index:
    :type leverage_index: playwright.sync_api._generated.ElementHandle
    :return:
    :rtype: pd.DataFrame
    """
    rects = leverage_index.query_selector_all(
        ".highcharts-series.highcharts-tracker > rect"
    )
    assert rects, leverage_index.inner_html()

    we_score_regex = re.compile(r"WE: (.*)% \| Score: (\d+) - (\d+)")

    for rect in rects:
        rect.hover()
        play = leverage_index.query_selector_all(
            ".highcharts-tooltip > text > tspan"
        )
        assert play, rect.inner_html()

        play_data = [e.text_content() for e in play]
        assert all(p for p in play_data)

        game_data, play_info = play_data[0], "\n".join(play_data[1:])
        win_expectancy, away_score, home_score = we_score_regex.search(
            game_data
        ).groups()
        assert all((win_expectancy, away_score, home_score))


def _test_scrape_game(game):
    """
    :py:func:`fangraphs.scores._scrape_game`

    :param game:
    :type game: playwright.sync_api._generated.ElementHandle
    :rtype: None
    """
    assert len(
        game.query_selector_all(
            "div.highcharts-container[id*='graph']"
        )
    ) == 2, game.inner_html()
    game_flow, leverage_index = game.query_selector_all(
        "div.highcharts-container[id*='graph']"
    )

    assert len(
        game_flow.query_selector_all(
            "text.highcharts-title > tspan"
        )
    ) == 1
    matchup = game_flow.query_selector(
        "text.highcharts-title > tspan"
    ).text_content()
    date, teams = matchup.split(" - ")

    date_dt = datetime.datetime.strptime(date, "%m/%d/%Y")
    assert date_dt

    teams_regex = re.compile(r"(.*)\((\d+)\) @ (.*)\((\d+)\)")
    away, away_score, home, home_score = teams_regex.search(teams).groups()
    away_score, home_score = int(away_score), int(home_score)
    assert all((away, away_score, home, home_score)), teams

    _test_scrape_leverage_index(leverage_index)


def _test_scrape_preview(preview):
    """
    :py:func:`fangraphs.scores._scrape_preview`

    :param preview:
    :type preview: playwright.sync_api._generated.ElementHandle
    :rtype: None
    """
    time_regex = re.compile(r"\d{1,2}:\d{1,2} ET")
    assert time_regex.search(preview.text_content())

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
