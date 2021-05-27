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


class TestLive(BaseTests):
    """
    :py:class:`fangraphs.scores.Live`
    """
    address = "https://www.fangraphs.com/livescoreboard.aspx"

    @staticmethod
    def _test_scrape_leverage_index(page, game_flow, leverage_index):
        """
        :py:meth:`fangraphs.scores.Live._scrape_charts`

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param game_flow:
        :type game_flow: playwright.sync_api._generated.ElementHandle
        :param leverage_index:
        :type leverage_index: playwright.sync_api._generated.ElementHandle
        :return:
        """
        game_flow.scroll_into_view_if_needed()
        leverage_index.scroll_into_view_if_needed()

        assert len(
            game_flow.query_selector_all(
                "div.highcharts-container > svg > rect[fill='white']"
            )
        ), game_flow.inner_html()
        bounds = page.query_selector(
            "div.highcharts-container > svg > rect[fill='white']"
        ).bounding_box()
        assert bounds

        assert len(
            game_flow.query_selector_all(
                "g.highcharts-markers.highcharts-tracker"
            )
        ) == 2, game_flow.inner_html()
        game_flow_tracker = game_flow.query_selector_all(
            "g.highcharts-markers.highcharts-tracker"
        )[1]

        we_regex = re.compile(r"WE: (.*%) | Score: (\d+) - (\d+)")
        game_flow_data = []
        xcoord, ycoord = bounds["x"], bounds["y"]-bounds["height"]
        for delta_x in range(int(bounds["width"])):
            page.mouse.move(xcoord, ycoord)
            grey_point = game_flow_tracker.query_selector("path[fill='#808080']")

            if grey_point.is_visible():
                ycoord = bounds["y"]-bounds["height"] if ycoord == bounds["y"] else bounds["y"]
                page.mouse.move(xcoord, ycoord)

            point = game_flow.query_selector(
                "g.highcharts-tooltip > text"
            )
            data = we_regex.search(
                point.query_selector("tspan:nth-child(1)").text_content()
            ).groups()
            info = "\n".join(
                [e.text_content() for e in point.query_selector_all("tspan")[1:]]
            )
            if (data, info) not in game_flow_data:
                game_flow_data.append((data, info))
        assert game_flow_data

    def _test_scrape_game(self, page, game):
        """
        :py:meth:`fangraphs.scores.Live._scrape_game`

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param game:
        :type game: playwright.sync_api._generated.ElementHandle
        :rtype: None
        """
        assert len(
            game.query_selector_all(
                "div.highcharts-container"
            )
        ) == 2, game.inner_html()
        game_flow, leverage_index = game.query_selector_all(
            "div.highcharts-container"
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

        self._test_scrape_leverage_index(page, game_flow, leverage_index)

    @staticmethod
    def _test_scrape_preview(preview):
        """
        :py:meth:`fangraphs.scores.Live._scrape_preview`

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
            "#LiveBoard1_LiveBoard1_litGamesPanel > table > tbody > tr > td[style*='vertical-align:top']"
        )

        for match in matches:
            if (
                len(match.query_selector_all("xpath=./div")) == 2
                and len(match.query_selector_all("xpath=./a")) == 3
            ):
                self._test_scrape_game(page, match)
            elif (
                len(match.query_selector_all("xpath=./b")) == 2
                and len(match.query_selector_all("xpath=./center")) == 1
            ):
                self._test_scrape_preview(match)
            else:
                raise AssertionError(
                    (len(match.query_selector_all("xpath=./div")),
                     len(match.query_selector_all("xpath=./a"))),
                    (len(match.query_selector_all("xpath=./b")),
                     len(match.query_selector_all("xpath=./center")))
                )
