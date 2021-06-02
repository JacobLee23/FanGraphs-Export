#! python3
# fangraphs/scores.py

"""
Scrapers for the webpages under the FanGraphs **Scores** tab.
"""

import datetime
import re

import pandas as pd

from fangraphs import ScrapingUtilities
from fangraphs.selectors import scores_sel


def _scrape_game(game):
    """
    Scrapes the matchup data for active games.

    :param game: The matchup element
    :type game: playwright.sync_api._generated.ElementHandle
    :return: The matchup name and a DataFrame of the matchup data
    :rtype: tuple[str, pd.DataFrame]
    """
    def get_hyperlink(elem):
        href = elem.get_attribute("href")
        hlink = href.replace(" ", "%20")
        return f"https://fangraphs.com/{hlink}"

    hyperlinks = (
        [e.text_content() for e in game.query_selector_all("xpath=./a")],
        [get_hyperlink(e) for e in game.query_selector_all("xpath=./a")]
    )

    links_dataframe = pd.DataFrame({"Links": hyperlinks})

    game_info = game.query_selector(
        "div[id*='graph']:nth-child(1) > div > svg > text.highcharts-title > tspan"
    )
    game_info_regex = re.compile(r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)")
    date, away_team, away_score, home_team, home_score = game_info_regex.search(
        game_info.text_content()
    ).groups()
    date_dt = datetime.datetime.strptime(date, "%m/%d/%Y")

    game_data_dataframe = pd.DataFrame(
        {
            "Date": date_dt,
            "Away": {
                "Team": away_team, "Score": away_score
            },
            "Home": {
                "Team": home_team, "Score": home_score
            }
        }
    )

    dataframe = pd.DataFrame(
        (game_data_dataframe, links_dataframe),
        index=("Game Data", "Links")
    )

    matchup = f"{away_team} @ {home_team}"

    return matchup, dataframe


def _scrape_preview(preview):
    """
    Scrapes the matchup data for game previews

    :param preview: The matchup element
    :type preview: playwright.sync_api._generated.ElementHandle
    :return: The matchup name and a DataFrame of the matchup data
    :rtype: tuple[str, pd.DataFrame]
    """
    away_team, home_team = [
        e.text_content() for e in preview.query_selector_all("b > a")
    ]
    matchup = f"{away_team} @ {home_team}"

    time_regex = re.compile(r"\d+:\d+ ET")
    time_dt = datetime.datetime.strptime(
        time_regex.search(preview.text_content()).group(),
        "%H:%M ET"
    )

    away_sp, home_sp, away_lineup, home_lineup = [
        e for e in preview.query_selector_all(
            "center > table.lineup tr > td"
        )
    ]
    away_sp, home_sp = (
        away_sp.text_content().split(": ")[1],
        home_sp.text_content().split(": ")[1]
    )

    pplayer_regex = re.compile(r"(\d+)\. (.*?) \((.*?)\)")

    away_lineup = {
        g[0]: {"Name": g[1], "Position": g[2]} for g in pplayer_regex.findall(
            away_lineup.text_content()
        )
    }
    home_lineup = {
        g[0]: {"Name": g[1], "Position": g[2]} for g in pplayer_regex.findall(
            home_lineup.text_content()
        )
    }
    away_lineup_df = pd.DataFrame(away_lineup)
    home_lineup_df = pd.DataFrame(home_lineup)

    dataframe = pd.DataFrame(
        {
            "Time": time_dt,
            "Away": {
                "Team": away_team,
                "Starting Pitcher": away_sp,
                "Starting Lineup": away_lineup_df
            },
            "Home": {
                "Team": home_team,
                "Starting Pitcher": home_sp,
                "Starting Lineup": home_lineup_df
            }
        }
    )
    return matchup, dataframe


class Live(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Live Scoreboard`_ page.

    .. _Live Scoreboard: https://www.fangraphs.com/livescoreboard.aspx
    """

    address = "https://www.fangraphs.com/livescoreboard.aspx"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.Live)

    def export(self):
        """
        Scrapes the matchup data for each matchup scheduled for the current date.

        The **Game Flow** and **Leverage Index** graph data are not scraped.
        For that data, use :py:class:`fangraphs.scores.WinProbability`.

        _Note: A '*' following the matchup name denotes a game preview._

        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        matches = self.page.query_selector_all(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table > tbody > tr > td[style*='border-bottom:1px dotted black;']"
        )

        data = {}
        for match in matches:
            if (
                    len(match.query_selector_all("xpath=./div")) == 2
                    and len(match.query_selector_all("xpath=./a")) == 3
            ):
                matchup, dataframe = _scrape_game(match)
                data.setdefault(matchup, dataframe)
            elif (
                    len(match.query_selector_all("xpath=./b")) == 2
                    and len(match.query_selector_all("xpath=./center")) == 1
            ):
                matchup, dataframe = _scrape_preview(match)
                data.setdefault(f"{matchup}*", dataframe)
        return data


class LiveLeaderboards(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Live Daily Leaderboards`_ page.

    .. _Live Daily Leaderboards: https://fangraphs.com/scores/live-leaderboards
    """
    address = "https://fangraphs.com/scores/live-leaderboards"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.LiveLeaderboards)
