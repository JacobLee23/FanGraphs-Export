#! usr/bin/env python
# fangraphs/scores.py

"""
Scrapers for the webpages under the FanGraphs **Scores** tab.
"""

import collections
import datetime
import re
from typing import *

import bs4
import pandas as pd

from fangraphs import FilterWidgets
from fangraphs import PID_REGEX, PID_POS_REGEX
from fangraphs.selectors import scores_


class LiveScoreboard(FilterWidgets):
    """
    Scraper for the FanGraphs `Live Scoreboard`_ page.

    .. _Live Scoreboard: https://www.fangraphs.com/livescoreboard.aspx
    """
    _widget_class = scores_.LiveScoreboard
    address = "https://www.fangraphs.com/livescoreboard.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self._matchup_tables = {}
        self.games = None
        self.previews = None

    @staticmethod
    def _scrape_game_data(match_table: bs4.Tag) -> pd.Series:
        """

        :param match_table:
        :return:
        """

        def get_hyperlink(elem: bs4.Tag) -> str:
            href = elem.get_attribute("href")
            hlink = href.replace(" ", "%20")
            return f"https://fangraphs.com/{hlink}"

        hyperlinks = dict(
            (e.text, get_hyperlink(e))
            for e in match_table.select(
                "a:nth-last-child(3),a:nth-last-child(2),a:nth-last-child(1)"
            )
        )

        game_info = match_table.select_one(
            "div[id*='graph']:first-child > div > svg > text.highcharts-title > tspan"
        )
        date, away_team, away_score, home_team, home_score = re.search(
            r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)", game_info.text
        )

        game_data = {
            "Matchup": f"{away_team} @ {home_team}",
            "Date": datetime.datetime.strptime(date, "%m/%d/%Y"),
            "Away Team": away_team, "Home Team": home_team,
            "Score": f"{away_score} - {home_score}",
            **hyperlinks
        }

        return pd.Series(game_data)

    @staticmethod
    def _scrape_preview_data(match_table: bs4.Tag) -> pd.Series:
        """

        :param match_table:
        :return:
        """
        def get_lineup(elem: bs4.Tag) -> dict[str, Union[str, pd.DataFrame]]:
            away_sp, home_sp, away_lineup, home_lineup = [
                e for e in elem.select("center > table.lineup tr > td")
            ]
            away_sp = away_sp.text.split(": ")[1]
            home_sp = home_sp.text.split(": ")[1]
            away_lineup = pd.DataFrame({
                g[0]: {"Name": g[1], "Position": g[2]} for g in re.findall(
                    r"(\d+)\. (.*?) \((.*?)\)", away_lineup.text
                )
            })
            home_lineup = pd.DataFrame({
                g[0]: {"Name": g[1], "Position": g[2]} for g in re.findall(
                    r"(\d+)\. (.*?) \((.*?)\)", home_lineup.text
                )
            })
            lineup = {
                "Away Starting Pitcher": away_sp,
                "Home Starting Pitcher": home_sp,
                "Away Starting Lineup": away_lineup,
                "Home Starting Lineup": home_lineup
            }
            return lineup

        time = re.search(r"\d+:\d+ ET", match_table.text).group()
        lineup_data = get_lineup(match_table)
        away_team, home_team = [
            e.text for e in match_table.select("b > a")
        ]

        preview_data = {
            "Matchup": f"{away_team} @ {home_team}",
            "Time": datetime.datetime.strptime(time, "%H:%M ET"),
            "Away Team": away_team, "Home Team": home_team,
            **lineup_data
        }

        return pd.Series(preview_data)

    @staticmethod
    def __refine_matchup_names(old: list[str]) -> list[str]:
        """

        :param old:
        :return:
        """

        counts = {x: 0 for x in old}
        new = []

        for matchup in old:
            if list(old).count(matchup) > 1:
                new.append(f"{matchup} ({counts[matchup]})")
                counts[matchup] += 1
            else:
                new.append(matchup)

        return new

    @property
    def _matchup_tables(self) -> dict[str, list[bs4.Tag]]:
        """

        :return:
        """
        return self.__matchup_tables

    @_matchup_tables.setter
    def _matchup_tables(self, value) -> None:
        table = self.soup.select_one(
            "#LiveBoard1_LiveBoard1_litGamesPanel > table:last-child"
        )
        matches = table.select(
            "tbody > td[style*='border-bottom:1px dotted black;']"
        )

        game_tables = {"Games": [], "Previews": []}
        for match in matches:
            if (
                    len(match.query_selector_all("xpath=./div")) == 2
                    and len(match.query_selector_all("xpath=./a")) == 3
            ):
                game_tables["Games"].append(match)
            elif (
                    len(match.query_selector_all("xpath=./b")) == 2
                    and len(match.query_selector_all("xpath=./center")) == 1
            ):
                game_tables["Previews"].append(match)

        self.__matchup_tables = game_tables

    @property
    def games(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._games

    @games.setter
    def games(self, value) -> None:
        game_series = []

        for gtable in self._matchup_tables["Games"]:
            game_series.append(self._scrape_game_data(gtable))

        matchup_names = self.__refine_matchup_names(
            [s["Matchup"] for s in game_series]
        )
        for gseries, mname in zip(game_series, matchup_names):
            gseries["Matchup"] = mname

        self._games = pd.DataFrame(game_series)

    @property
    def previews(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._previews

    @previews.setter
    def previews(self, value) -> None:
        preview_series = []

        for ptable in self._matchup_tables["Previews"]:
            preview_series.append(self._scrape_preview_data(ptable))

        matchup_names = self.__refine_matchup_names(
            [s["Matchup"] for s in preview_series]
        )
        for pseries, mname in zip(preview_series, matchup_names):
            pseries["Matchup"] = mname

        self._previews = pd.DataFrame(preview_series)


class LiveLeaderboards(FilterWidgets):
    """
    Scraper for the FanGraphs `Live Daily Leaderboards`_ page.

    .. _Live Daily Leaderboards: https://fangraphs.com/scores/live-leaderboards
    """
    _widget_class = scores_.LiveLeaderboards
    address = "https://fangraphs.com/scores/live-leaderboards"

    def __init__(self, *, table_size="Infinity", **kwargs):
        """

        """
        FilterWidgets.__init__(self, table_size=table_size, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        table = self.soup.select_one(".table-fixed > table")

        def get_team_homeaway(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select_one(
                    "td[data-stat='Opp'] > div.game-desc > a"
                )
                yield "Away" if "@" in elem.text else "Home"

        def get_score(row_elems: bs4.ResultSet) -> Generator[
            tuple[int, int], None, None
        ]:
            for row in row_elems:
                elem = row.select_one(
                    "td[data-stat='Opp'] > div.game-desc > div.game-info"
                )
                yield re.search(r"(\d+-\d+)", elem.text).group()

        def get_final(row_elems: bs4.ResultSet) -> Generator[
            bool, None, None
        ]:
            for row in row_elems:
                elem = row.select_one(
                    "td[data-stat='Opp'] > div.game-desc > div.game-info"
                )
                yield True if "(F)" in elem.text else False

        def get_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select_one("td[data-stat='Name'] > a")
                yield PID_REGEX.search(
                    elem.attrs.get("href")
                ).group(1)

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe.drop(columns=dataframe.columns[0], inplace=True)
        dataframe["Home/Away"] = tuple(get_team_homeaway(table_data.row_elems))
        dataframe["Score"] = tuple(get_score(table_data.row_elems))
        dataframe["Final"] = tuple(get_final(table_data.row_elems))
        dataframe["PlayerID"] = tuple(get_player_id(table_data.row_elems))

        self._data = dataframe


class Scoreboard(FilterWidgets):
    """
    Scraper for the FanGraphs `Scoreboard`_ page.

    .. _Scoreboard: https://fangraphs.com/scoreboard.aspx
    """
    _widget_class = scores_.Scoreboard
    address = "https://fangraphs.com/scoreboard.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @staticmethod
    def _scrape_matchup_data(match_table: bs4.Tag) -> pd.Series:
        """

        :param match_table:
        :return:
        """

        def get_hyperlink(elem: bs4.Tag) -> str:
            href = elem.get_attribute("href")
            hlink = href.replace(" ", "%20")
            return f"https://fangraphs.com/{hlink}"

        hyperlinks = dict(
            (e.text, get_hyperlink(e))
            for e in match_table.select(
                "a:nth-last-child(3),a:nth-last-child(2),a:nth-last-child(1)"
            )
        )

        game_info = match_table.select_one(
            "div[id*='graph']:first-child > div > svg > text.highcharts-title > tspan"
        )
        date, away_team, away_score, home_team, home_score = re.search(
            r"(.*) - (.*)\((\d+)\) @ (.*)\((\d+)\)", game_info.text
        )

        game_data = {
            "Matchup": f"{away_team} @ {home_team}",
            "Date": datetime.datetime.strptime(date, "%m/%d/%Y"),
            "Away Team": away_team, "Home Team": home_team,
            "Score": f"{away_score} - {home_score}",
            **hyperlinks
        }

        return pd.Series(game_data)

    @staticmethod
    def __refine_matchup_names(old: list[str]) -> list[str]:
        """

        :param old:
        :return:
        """

        counts = {x: 0 for x in old}
        new = []

        for matchup in old:
            if list(old).count(matchup) > 1:
                new.append(f"{matchup} ({counts[matchup]})")
                counts[matchup] += 1
            else:
                new.append(matchup)

        return new

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        table = self.soup.select_one(
            "#content > table > tbody > tr > td > table:last-child"
        )
        matches = table.select(
            "tbody > td[style*='border-bottom:1px dotted black;']"
        )

        matchup_series = []
        for mtable in matches:
            matchup_series.append(self._scrape_matchup_data(mtable))

        matchup_names = self.__refine_matchup_names(
            [s["Matchup"] for s in matchup_series]
        )
        for gseries, mname in zip(matchup_series, matchup_names):
            gseries["Matchup"] = mname

        self._data = pd.DataFrame(matchup_series)


class GameGraphs(FilterWidgets):
    """
    Scraper for the FanGraphs `Game Graphs`_ tab of the game pages.

    .. _Game Graphs: https://fangraphs.com/wins.aspx
    """
    _widget_class = scores_.GameGraphs
    address = "https://fangraphs.com/wins.aspx"

    class BoxScore(NamedTuple):
        away_batting: pd.DataFrame
        home_batting: pd.DataFrame
        away_pitching: pd.DataFrame
        home_pitching: pd.DataFrame

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.stars_of_the_game = None
        self.box_score = ()

    @property
    def stars_of_the_game(self) -> pd.Series:
        """

        :return:
        """
        return self._stars_of_the_game

    @stars_of_the_game.setter
    def stars_of_the_game(self, value) -> None:
        table = self.soup.select_one(
            "#WinsGame1_ThreeStars1_ajaxPanel > #pan1"
        )
        sotgs = [
            e.text.strip() for e in table.select("tr > td:first-child")[1:]
        ]

        data = {1: None, 2: None, 3: None}
        for i, player in enumerate(reversed(sotgs), 1):
            if (m := re.search(r"(.*) \((.*) / (.*)\)", player)) is not None:
                data[i] = m.groups()

        self._stars_of_the_game = pd.Series(data)

    @property
    def box_score(self) -> BoxScore:
        """

        :return:
        """
        return self._box_score

    @box_score.setter
    def box_score(self, value) -> None:
        tables = self.soup.select(
            "div.RadGrid.RadGrid_FanGraphs > table.rgMasterTable"
        )
        table_names = (
            "Away Pitching", "Home Pitching", "Away Batting", "Home Batting"
        )

        data = {}
        for table, tname in zip(tables, table_names):
            table_data = self.scrape_table(table)
            data["_".join(tname.lower().split())] = table_data.dataframe

        self._box_score = self.BoxScore(**data)


class PlayLog(FilterWidgets):
    """
    Scraper for the FanGraphs `Play Log`_ tab of the game pages.

    .. _Play Log: https://fangraphs.com/plays.aspx
    """
    _widget_class = scores_.PlayLog
    address = "https://fangraphs.com/plays.aspx"

    def __init__(self, **kwargs):
        """

        """
        FilterWidgets.__init__(self, **kwargs)

        self.data = None

    @property
    def data(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._data

    @data.setter
    def data(self, value) -> None:
        table = self.soup.select_one(".table-scroll > table")

        def get_inning(row_elems: bs4.ResultSet) -> Generator[
            tuple[int, str], None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[1]
                yield re.search(r"\d+", elem.text).group()

        def get_topbottom(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[1]
                yield re.search(r"[▲▼]", elem.text).group()

        def get_batter_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[2].select_one("a")
                yield PID_REGEX.search(
                    elem.attrs.get("href")
                ).group(1)

        def get_pitcher_player_id(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[3].select_one("a")
                yield PID_REGEX.search(
                    elem.attrs.get("href")
                ).group(1)

        def get_play(row_elems: bs4.ResultSet) -> Generator[
            str, None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[7].select_one(".play-desc-text")
                yield elem.text

        def get_pitch_sequence(row_elems: bs4.ResultSet) -> Generator[
            Optional[str], None, None
        ]:
            for row in row_elems:
                elem = row.select("td")[7].select_one(".play-desc-pitch-seq")
                yield tuple(elem.text.split(", ")) if elem is not None else None

        table_data = self.scrape_table(table)

        dataframe = table_data.dataframe
        dataframe.drop(columns=dataframe.columns[0], inplace=True)
        dataframe.insert(
            loc=8, column="Pitch Sequence", value=tuple(
                get_pitch_sequence(table_data.row_elems)
            )
        )
        dataframe.insert(
            loc=2, column="Top/Bottom", value=tuple(
                get_topbottom(table_data.row_elems)
            )
        )
        dataframe.insert(
            loc=2, column="Inning", value=tuple(
                get_inning(table_data.row_elems)
            )
        )
        dataframe["Batter PlayerID"] = tuple(
            get_batter_player_id(table_data.row_elems)
        )
        dataframe["Pitcher PlayerID"] = tuple(
            get_pitcher_player_id(table_data.row_elems)
        )
        dataframe["Play"] = tuple(
            get_play(table_data.row_elems)
        )

        self._data = dataframe


class BoxScore(FilterWidgets):
    """
    Scrapes the FanGraphs `Box Score`_ pages.

    .. _Box Score: https://fangraphs.com/boxscore.aspx
    """
    _widget_class = scores_.BoxScore

    address = "https://fangraphs.com/boxscore.aspx"

    def __init__(self, **kwargs):
        FilterWidgets.__init__(self, **kwargs)

        self._tables = None

        self.line_score = None
        self.play_by_play = None
        self.data_tables = None

    @property
    def _tables(self) -> bs4.ResultSet:
        """

        :return:
        """
        return self.__tables

    @_tables.setter
    def _tables(self, value) -> None:
        """

        """
        if value is not None:
            return
        self.__tables = self.soup.select("div.RadGrid.RadGrid_FanGraphs")

    @property
    def line_score(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._line_score

    @line_score.setter
    def line_score(self, value) -> None:
        """

        """
        table = self.soup.select_one(
            "div.scoreboard-wrapper > table.linescore"
        )
        header_elems = table.select(
            "thead > tr.linescore-header > th"
        )
        headers = [e.text for e in header_elems][1:]
        headers.insert(0, "Team")
        dataframe = pd.DataFrame(columns=headers)

        row_elems = table.select("tbody > tr.team")
        for team, row in zip(("Away", "Home"), row_elems):
            elems = row.select("td")
            items = [e.text for e in elems]
            dataframe.loc[team] = items

        self._line_score = dataframe

    @property
    def play_by_play(self) -> pd.DataFrame:
        """

        :return:
        """
        return self._play_by_play

    @play_by_play.setter
    def play_by_play(self, value) -> None:
        """

        """
        pbp_table = self._tables[4]
        header_elems = pbp_table.select("thead > tr > th")
        row_elems = pbp_table.select("tbody > tr")

        dataframe = pd.DataFrame(
            data=[
                [e.text for e in r.select("td")]
                for r in row_elems
            ],
            columns=[e.text for e in header_elems]
        )
        dataframe.drop(columns=dataframe.columns[-2:])

        def pitch_sequence() -> list[list[str]]:
            items = []
            for row in row_elems:
                elem = row.select_one("td:nth-child(7) a")
                if elem is not None:
                    pitches = elem.attrs.get("tooltip").split(",")
                else:
                    pitches = []
                items.append(pitches)
            return items

        dataframe["Pitch Sequence"] = pitch_sequence()
        dataframe["Player ID (Pitcher)"] = [
            PID_POS_REGEX.search(
                r.select_one("td:nth-child(1) a").attrs.get("href")
            ).group(1) for r in row_elems
        ]
        dataframe["Player ID (PLayer)"] = [
            PID_POS_REGEX.search(
                r.select_one("td:nth-child(2) a").attrs.get("href")
            ).group(1) for r in row_elems
        ]

        self._play_by_play = dataframe

    @staticmethod
    def _scrape_table(table: bs4.Tag) -> pd.DataFrame:
        """

        :param table:
        :return:
        """
        header_elems = table.select("thead > tr > th.rgHeader")
        row_elems = table.select("tbody > tr")
        dataframe = pd.DataFrame(
            data=[
                [e.text for e in r.select("td")]
                for r in row_elems
            ],
            columns=[e.text for e in header_elems]
        )

        def playerids_positions() -> [list[str], list[str]]:
            player_ids, positions, = [], []
            for row in row_elems:
                elem = row.select_one("td:nth-child(1)")
                if elem.text != "Total":
                    pid, position = PID_POS_REGEX.search(
                        elem.select_one("a").attrs.get("href")
                    ).groups()
                else:
                    pid, position = "", ""
                player_ids.append(pid)
                positions.append(position)
            return player_ids, positions

        dataframe["Player ID"], dataframe["Position"] = playerids_positions()

        return dataframe

    @property
    def data_tables(self) -> NamedTuple:
        """

        :return:
        """
        return self._data_tables

    @data_tables.setter
    def data_tables(self, value) -> None:
        """

        """

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
