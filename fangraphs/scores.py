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


def __refine_matchup_names(old: list[str]):
    """

    :param old:
    :return:
    :rtype: list[str]
    """
    counts = dict(zip(s := set(old), [0] * len(s)))
    new = []

    for matchup in old:
        if list(old).count(matchup) > 1:
            new.append(f"{matchup} ({counts[matchup]})")
            counts[matchup] += 1
        else:
            new.append(matchup)

    return new


def _scrape_game_data(games):
    """
    Scrapes the matchup data for active games.

    :param games:
    :type games: list[playwright.sync_api._generated.ElementHandle
    :return:
    :rtype: pd.DataFrame
    """
    def get_hyperlink(elem):
        href = elem.get_attribute("href")
        hlink = href.replace(" ", "%20")
        return f"https://fangraphs.com/{hlink}"

    names, data = [], []
    for game in games:
        hyperlinks = dict(
            [(e.text_content(), get_hyperlink(e)) for e in game.query_selector_all("xpath=./a")]
        )
        game_info = game.query_selector(
            "div[id*='graph']:nth-child(1) > div > svg > text.highcharts-title > tspan"
        )
        game_info_regex = re.compile(r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)")
        date, away_team, away_score, home_team, home_score = game_info_regex.search(
            game_info.text_content()
        ).groups()
        date_dt = datetime.datetime.strptime(date, "%m/%d/%Y")

        game_data = {
            "Date": date_dt,
            "Away Team": away_team,
            "Home Team": home_team,
            "Score": f"{away_score} - {home_score}",
        }
        game_data.update(hyperlinks)

        names.append(f"{away_team} @ {home_team}")
        data.append(game_data)

    names = __refine_matchup_names(names)

    dataframe = pd.DataFrame(
        dict(zip(names, data)),
        index=[
            "Date", "Away Team", "Home Team", "Score", "Box Score",
            "Win Probability", "Play Log"
        ]
    )

    return dataframe


def _scrape_preview_data(previews):
    """
    Scrapes the matchup data for game previews

    :param previews: The matchup element
    :type previews: list[playwright.sync_api._generated.ElementHandle]
    :return:
    :rtype:
    """
    time_regex = re.compile(r"\d+:\d+ ET")
    pplayer_regex = re.compile(r"(\d+)\. (.*?) \((.*?)\)")

    names, data = [], []
    for preview in previews:
        time_dt = datetime.datetime.strptime(
            time_regex.search(preview.text_content()).group(), "%H:%M ET"
        )

        away_team, home_team = [
            e.text_content() for e in preview.query_selector_all("b > a")
        ]

        away_sp, home_sp, away_lineup, home_lineup = [
            e for e in preview.query_selector_all(
                "center > table.lineup tr > td"
            )
        ]
        away_sp, home_sp = (
            away_sp.text_content().split(": ")[1], home_sp.text_content().split(": ")[1]
        )

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

        preview_data = {
            "Time": time_dt,
            "Away Team": away_team,
            "Home Team": home_team,
            "Away Starting Pitcher": away_sp,
            "Home Starting Pitcher": home_sp,
            "Away Starting Lineup": pd.DataFrame(away_lineup),
            "Home Starting Lineup": pd.DataFrame(home_lineup)
        }

        names.append(f"{away_team} @ {home_team}")
        data.append(preview_data)

    names = __refine_matchup_names(names)

    dataframe = pd.DataFrame(
        dict(zip(names, data)),
        index=[
            "Time", "Away Team", "Home Team", "Away Starting Pitcher",
            "Home Starting Pitcher", "Away Starting Lineup",
            "Away Starting Lineup", "Home Starting Lineup"
        ]
    )

    return dataframe


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
        table_body = self.page.query_selector(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table:nth-last-child(1) > tbody"
        )
        matches = table_body.query_selector_all(
            "td[style*='border-bottom:1px dotted black;']"
        )

        games, previews = [], []
        for match in matches:
            if (
                    len(match.query_selector_all("xpath=./div")) == 2
                    and len(match.query_selector_all("xpath=./a")) == 3
            ):
                games.append(match)
            elif (
                    len(match.query_selector_all("xpath=./b")) == 2
                    and len(match.query_selector_all("xpath=./center")) == 1
            ):
                previews.append(match)

        games_df = _scrape_game_data(games)
        previews_df = _scrape_preview_data(previews)
        data = {"Games": games_df, "Previews": previews_df}

        return data


class LiveLeaderboards(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Live Daily Leaderboards`_ page.

    .. _Live Daily Leaderboards: https://fangraphs.com/scores/live-leaderboards
    """
    address = "https://fangraphs.com/scores/live-leaderboards"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.LiveLeaderboards)

    @staticmethod
    def _scrape_table_headers(table):
        """

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        :return:
        :rtype: list[str]
        """
        header_elems = table.query_selector_all("thead > tr > th")[1:]
        headers = [e.text_content() for e in header_elems]
        headers.insert(3, "Score")
        headers.insert(2, "Home/Away")
        headers.insert(1, "Player ID")

        return headers

    @staticmethod
    def _scrape_table_rows(table):
        """

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        :return:
        :rtype: list[str]
        """
        rows = table.query_selector_all("tbody > tr")

        href_regex = re.compile(r"//www.fangraphs.com/statss.aspx\?playerid=(.*)")
        opp_regex = re.compile(r"(@)?(.*)(\d+-\d+ \((F|Top|Bottom) \d+\))")

        for i, row in enumerate(rows):
            elems = row.query_selector_all("td")[1:]

            data = [e.text_content() for e in elems]

            href = elems[0].query_selector("a").get_attribute("href")
            player_id = href_regex.search(href).group(1)

            home_away, opp, score, _ = opp_regex.search(data[2]).groups()
            home_away = "Away" if home_away is not None else "Home"
            data[2] = opp

            data.insert(3, score)
            data.insert(2, home_away)
            data.insert(1, player_id)

            yield data

    def export(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        table = self.page.query_selector(".table-fixed > table")
        headers = self._scrape_table_headers(table)
        rows = self._scrape_table_rows(table)

        dataframe = pd.DataFrame(columns=headers)
        for i, row in enumerate(rows):
            dataframe.loc()[i] = row

        return dataframe


class Scoreboard(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Scoreboard`_ page.

    .. _Scoreboard: https://fangraphs.com/scoreboard.aspx
    """
    address = "https://fangraphs.com/scoreboard.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.Scoreboard)

    def export(self):
        """

        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        table_body = self.page.query_selector(
            "#content > table > tbody > tr > td > table:nth-last-child(1) > tbody"
        )
        matches = table_body.query_selector_all(
            "td[style*='border-bottom:1px dotted black;']"
        )

        games_dataframe = _scrape_game_data(matches)
        return games_dataframe


class GameGraphs(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Game Graphs`_ tab of the game pages.

    .. _Game Graphs: https://fangraphs.com/wins.aspx
    """
