#! python3
# fangraphs/scores.py

"""
Scrapers for the webpages under the FanGraphs **Scores** tab.
"""

import collections
import datetime
import re

import pandas as pd
from playwright.sync_api import sync_playwright

from fangraphs import ScrapingUtilities
from fangraphs import PID_REGEX, PID_POS_REGEX
from fangraphs.selectors import scores_sel


def _scrape_sotg(page):
    """

    :param page: A Playwright ``Page`` object
    :type page: playwright.sync_api._generated.Page
    :return: 
    :rtype: pd.DataFrame
    """
    sotg_regex = re.compile(r"(.*) \((.*) / (.*)\)")

    sotg_table = page.query_selector(
        "#WinsGame1_ThreeStars1_ajaxPanel > #pan1"
    )
    sotgs = sotg_table.query_selector_all("tr > td:nth-child(1)")[1:]
    stars_of_the_game = [e.text_content().strip() for e in sotgs]

    dataframe = pd.DataFrame(columns=[1, 2, 3])
    for i, player in enumerate(reversed(stars_of_the_game), 1):
        data = [None, None, None]
        match = sotg_regex.search(player)
        if match is not None:
            data = match.groups()

        dataframe.loc[i] = data

    return dataframe


def _scrape_table_headers(table):
    """

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    :return:
    :rtype: pd.DataFrame
    """
    elems = table.query_selector_all("thead > tr > th")
    headers = [e.text_content() for e in elems]
    headers.insert(1, "Player ID")

    dataframe = pd.DataFrame(columns=headers[1:])
    return dataframe


def _scrape_table(table):
    """

    :param table:
    :type table: playwright.sync_api._generated.ElementHandle
    :return:
    :rtype: pd.DataFrame
    """
    dataframe = _scrape_table_headers(table)

    rows = table.query_selector_all("tbody > tr")[:-1]

    for i, row in enumerate(rows):
        elems = row.query_selector_all("td")
        items = [e.text_content() for e in elems]

        href = elems[0].query_selector("a").get_attribute("href")
        player_id = PID_POS_REGEX.search(href).group(1)

        items.insert(1, player_id)

        dataframe.loc[items[0]] = items[1:]

    return dataframe


def __refine_matchup_names(old):
    """

    :param old:
    :type old: list[str]
    :return:
    :rtype: list[str]
    """

    counts = dict(zip(set(old), [0] * len(old)))
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

        opp_regex = re.compile(r"(@)?(.*)(\d+-\d+ \((F|Top \d+|Bot \d+)\))")

        for i, row in enumerate(rows):
            elems = row.query_selector_all("td")[1:]

            data = [e.text_content() for e in elems]

            href = elems[0].query_selector("a").get_attribute("href")
            player_id = PID_REGEX.search(href).group(1)

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
    address = "https://fangraphs.com/wins.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.GameGraphs)

    def export(self):
        """

        :return: 
        :rtype: dict[str, pd.DataFrame]
        """
        stars_of_the_game = _scrape_sotg(self.page)

        table_names = (
            "Away Pitching",
            "Home Pitching",
            "Away Batting",
            "Home Batting"
        )
        table_data = []
        tables = self.page.query_selector_all(
            "div.RadGrid.RadGrid_FanGraphs > table.rgMasterTable"
        )
        for table in tables:
            table_data.append(_scrape_table(table))
        
        data = dict(zip(table_names, table_data))
        data.update({"Stars of the Game": stars_of_the_game})

        return data


class PlayLog(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Play Log`_ tab of the game pages.

    .. _Play Log: https://fangraphs.com/plays.aspx
    """
    address = "https://fangraphs.com/plays.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, scores_sel.PlayLog)

    @staticmethod
    def _scrape_headers(table):
        """

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        :return:
        :rtype: pd.DataFrame
        """
        elems = table.query_selector_all("thead > tr > th")
        headers = [e.text_content() for e in elems]
        headers.insert(8, "Pitch Sequence")
        headers.insert(4, "Pitcher Player ID")
        headers.insert(3, "Batter Player ID")
        headers.insert(2, "Top/Bot")
        headers.insert(2, "Inning")

        dataframe = pd.DataFrame(columns=headers[1:])
        return dataframe

    def _scrape_table(self, table):
        """

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        :return:
        """
        dataframe = self._scrape_headers(table)

        rows = table.query_selector_all("tbody > tr")

        inning_regex = re.compile(r"([▲▼]) (\d+)")

        for row in rows:
            elems = row.query_selector_all("td")
            items = [e.text_content() for e in elems]

            top_bot, inning = inning_regex.search(items[1]).groups()
            if top_bot.encode() == b'\xe2\x96\xb2':
                inn_half = "Top"
            elif top_bot.encode() == b'\xe2\x96\xbc':
                inn_half = "Bot"
            else:
                continue

            batter_id, pitcher_id = [
                PID_REGEX.search(
                    e.query_selector("a").get_attribute("href")
                ).group(1) for e in elems[2:4]
            ]

            items[7] = elems[7].query_selector(
                ".play-desc-text"
            ).text_content()
            pitch_seq = elems[7].query_selector(
                ".play-desc-pitch-seq"
            )
            pitch_sequence = pitch_seq.text_content() if pitch_seq is not None else None

            items.insert(8, pitch_sequence)
            items.insert(4, pitcher_id)
            items.insert(3, batter_id)
            items.insert(2, inn_half)
            items.insert(2, inning)

            dataframe.loc[int(items[0])] = items[1:]

        return dataframe

    def export(self):
        """

        :return: pd.DataFrame
        """
        table = self.page.query_selector(".table-scroll > table")
        dataframe = self._scrape_table(table)
        return dataframe


class BoxScore(ScrapingUtilities):
    """
    Scrapes the FanGraphs `Box Score`_ pages.

    .. _Box Score: https://fangraphs.com/boxscore.aspx
    """
    address = "https://fangraphs.com/boxscore.aspx"

    def __init__(self, browser):
        """
        :type browser: playwright.sync_api._generated.Browser
        """
        # ScrapingUtilities.__init__(self, browser, self.address, scores_sel.BoxScore)
        self.__play = sync_playwright().start()
        self.__browser = self.__play.chromium.launch()
        self.page = self.__browser.new_page()
        self.page.goto(self.address, timeout=0)

        self._tables = None

        self.line_score = None
        self.play_by_play = None
        self.data_tables = None

    def __del__(self):
        self.__browser.close()
        self.__play.stop()

    @property
    def _tables(self):
        """

        :return:
        :rtype: list[playwright.sync_api._generated.ElementHandle]
        """
        return self.__tables

    @_tables.setter
    def _tables(self, value) -> None:
        """

        """
        if value is not None:
            return
        self.__tables = self.page.query_selector_all(
            "div.RadGrid.RadGrid_FanGraphs"
        )

    @property
    def line_score(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        return self._line_score

    @line_score.setter
    def line_score(self, value) -> None:
        """

        """
        if value is not None:
            return

        table = self.page.query_selector(
            "div.scoreboard-wrapper > table.linescore"
        )
        header_elems = table.query_selector_all(
            "thead > tr.linescore-header > th"
        )
        headers = [e.text_content() for e in header_elems][1:]
        headers.insert(0, "Team")
        dataframe = pd.DataFrame(columns=headers)

        row_elems = table.query_selector_all("tbody > tr.team")
        for team, row in zip(("Away", "Home"), row_elems):
            elems = row.query_selector_all("td")
            items = [e.text_content() for e in elems]
            dataframe.loc[team] = items

        self._line_score = dataframe

    @property
    def play_by_play(self):
        """

        :return:
        :rtype: pd.DataFrame
        """
        return self._play_by_play

    @play_by_play.setter
    def play_by_play(self, value) -> None:
        """

        :param value:
        """
        if value is not None:
            return

        pbp_table = self._tables[4]
        header_elems = pbp_table.query_selector_all("thead > tr > th")
        row_elems = pbp_table.query_selector_all("tbody > tr")

        dataframe = pd.DataFrame(
            data=[
                [e.text_content() for e in r.query_selector_all("td")]
                for r in row_elems
            ],
            columns=[e.text_content() for e in header_elems]
        )
        dataframe.drop(columns=dataframe.columns[-2:])

        def pitch_sequence() -> list[list[str]]:
            items = []
            for row in row_elems:
                elem = row.query_selector("td:nth-child(7) a")
                if elem is not None:
                    pitches = elem.get_attribute("tooltip").split(",")
                else:
                    pitches = []
                items.append(pitches)
            return items

        dataframe["Pitch Sequence"] = pitch_sequence()
        dataframe["Player ID (Pitcher)"] = [
            PID_POS_REGEX.search(
                r.query_selector("td:nth-child(1) a").get_attribute("href")
            ).group(1) for r in row_elems
        ]
        dataframe["Player ID (PLayer)"] = [
            PID_POS_REGEX.search(
                r.query_selector("td:nth-child(2) a").get_attribute("href")
            ).group(1) for r in row_elems
        ]

        self._play_by_play = dataframe

    @staticmethod
    def _scrape_table(table):
        """

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        :return:
        :rtype: pd.DataFrame
        """
        header_elems = table.query_selector_all("thead > tr > th.rgHeader")
        row_elems = table.query_selector_all("tbody > tr")
        dataframe = pd.DataFrame(
            data=[
                [e.text_content() for e in r.query_selector_all("td")]
                for r in row_elems
            ],
            columns=[e.text_content() for e in header_elems]
        )

        def playerids_positions() -> [list[str], list[str]]:
            player_ids, positions, = [], []
            for row in row_elems:
                elem = row.query_selector("td:nth-child(1)")
                if elem.text_content() != "Total":
                    pid, position = PID_POS_REGEX.search(
                        elem.query_selector("a").get_attribute("href")
                    ).groups()
                else:
                    pid, position = "", ""
                player_ids.append(pid)
                positions.append(position)
            return player_ids, positions

        dataframe["Player ID"], dataframe["Position"] = playerids_positions()

        return dataframe

    @property
    def data_tables(self):
        """

        :return:
        :rtype: dict[str, pd.DataFrame]
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, value):
        if value is not None:
            return

        table_names = (
            "box_score", "dashboard", "standard", "advanced", "batted_ball",
            "more_batted_ball", "win_probability", "pitch_type",
            "pitch_value", "plate_discipline"
        )
        stat_groups = (
            "batting_away", "batting_home", "pitching_away", "pitching_home"
        )
        DataTables = collections.namedtuple("DataTables", table_names)
        StatGroups = collections.namedtuple("StatGroups", stat_groups)

        data = {a: {b: None for b in stat_groups} for a in table_names}

        tables = self._tables[:4] + self._tables[5:]
        table_groups = [
            tables[i:(i+4)] for i in range(0, len(tables), 4)
        ]
        for dtables, tname in zip(table_groups, table_names):
            for table, tstat in zip(dtables, stat_groups):
                data[tname][tstat] = self._scrape_table(table)
            self.__setattr__(tname, StatGroups(**data[tname]))

        data_tables = DataTables(
            **{a: StatGroups(
                **{b: data[a][b] for b in stat_groups}
            ) for a in table_names}
        )

        self._data_tables = data_tables
