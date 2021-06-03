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

    names, dataframes = [], []
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
        dataframes.append(game_data)

    counts = dict(zip(s := set(names), [0]*len(s)))
    matchup_names = []
    for matchup in names:
        if list(names).count(matchup) > 1:
            matchup_names.append(f"{matchup} ({counts[matchup]})")
            counts[matchup] += 1
        else:
            matchup_names.append(matchup)

    dataframe = pd.DataFrame(
        dict(zip(matchup_names, dataframes)),
        index=[
            "Date", "Away Team", "Home Team", "Score", "Box Score",
            "Win Probability", "Play Log"
        ]
    )

    return dataframe


def _scrape_game(game):
    """
    Scrapes the matchup data for active games.

    :param game: The matchup element
    :type game: playwright.sync_api._generated.ElementHandle
    :return: The matchup name and a Series of the matchup data
    :rtype: tuple[str, pd.series]
    """
    def get_hyperlink(elem):
        href = elem.get_attribute("href")
        hlink = href.replace(" ", "%20")
        return f"https://fangraphs.com/{hlink}"

    hyperlinks = dict(zip(
        [e.text_content() for e in game.query_selector_all("xpath=./a")],
        [get_hyperlink(e) for e in game.query_selector_all("xpath=./a")]
    ))

    game_info = game.query_selector(
        "div[id*='graph']:nth-child(1) > div > svg > text.highcharts-title > tspan"
    )
    game_info_regex = re.compile(r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)")
    date, away_team, away_score, home_team, home_score = game_info_regex.search(
        game_info.text_content()
    ).groups()
    date_dt = datetime.datetime.strptime(date, "%m/%d/%Y")

    data = {
        "Date": date_dt,
        "Away Team": away_team,
        "Home Team": home_team,
        "Score": f"{away_score} - {home_score}",
    }
    data.update(hyperlinks)
    series = pd.Series(data)

    matchup = f"{away_team} @ {home_team}"

    return matchup, series


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
        table_body = self.page.query_selector(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table:nth-last-child(1) > tbody"
        )
        matches = table_body.query_selector_all(
            "td[style*='border-bottom:1px dotted black;']"
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
