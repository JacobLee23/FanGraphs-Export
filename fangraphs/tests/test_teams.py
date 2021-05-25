#! python3
# fangraphs/tests/test_teams.py

"""
Unit tests for :py:mod:`fangraphs.teams`.
"""

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
def summary_page():
    return TestSummary.address


@pytest.fixture(scope="module")
def stats_page():
    return TestStats.address


@pytest.fixture(scope="module")
def schedule_page():
    return TestSchedule.address


@pytest.fixture(scope="module")
def playerusage_page():
    return TestPlayerUsage.address


@pytest.fixture(scope="module")
def depthchart_page():
    return TestDepthChart.address


def _test_get_table_headers(table):
    """
    :py:func:`fangraphs.teams._get_table_headers`

    :param table: The element of the stat leaders data header_elem
    :type table: playwright.sync_api._generated.ElementHandle
    """
    elems = table.query_selector_all("thead > tr > th")
    assert elems, table.inner_html()
    headers = [e.text_content() for e in elems]
    assert all(headers), table.inner_html()


def _test_scrape_data_table(table):
    """
    :py:func:`fangraphs.teams._scrape_data_table`

    :param table: The element of the stat leaders data header_elem
    :type table: playwright.sync_api._generated.ElementHandle
    """
    _test_get_table_headers(table)

    rows = table.query_selector_all("tbody > tr[role='row']")
    assert rows, table.inner_html()
    href_regex = re.compile(r"/statss\.aspx\?playerid=(\d+)&position=(.*)")

    for i, row in enumerate(rows):
        subelems = row.query_selector_all("td")
        assert subelems, (i, row.inner_html())
        data = [e.text_content() for e in subelems]
        assert data, (i, row.inner_html())

        assert len(
            row.query_selector_all("td.frozen > a")
        ) == 1, row.inner_html()
        href = row.query_selector("td.frozen > a").get_attribute("href")
        assert href, (i, row.inner_html())
        assert href_regex.search(href).groups(), (i, href)


def _test_scrape_depth_chart(page, pos_nums):
    """
    :py:func:`fangraphs.teams._scrape_depth_chart`

    :param page:
    :type page: playwright.sync_api._generated.Page
    :param pos_nums: A sequence of positional numbers to scrape
    """
    href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

    for i in pos_nums:
        pos_name, player_stats = _test_scrape_positional_data(page, i)

        for j, (player, stat) in enumerate(player_stats):
            player_name, stat_value = player.text_content(), stat.text_content()
            assert (player_name and stat_value)

            assert len(
                player.query_selector_all("a")
            ) == 1, (player_name, stat_value)
            href = player.query_selector("a").get_attribute("href")
            assert href, (player_name, stat_value)
            player_id = href_regex.search(href)
            assert player_id, href


def _test_scrape_positional_data(page, pos_num: int):
    """

    :param page: A Playwright ``Page`` object
    :type page: playwright.sync_api._generated.Page
    :param pos_num: The positional number
    :return: The position name and the zipped player names and stats
    :rtype: tuple[
        list[str], list[tuple[playwright.sync_api._generated.ElementHandle]]
    ]
    """
    position = page.query_selector(f"#pos{pos_num}")
    assert position, page.url
    assert len(
        position.query_selector_all(
            f"text#pos-label{pos_num}"
        )
    ) == 1, position.inner_html()

    pos_name = position.query_selector(f"text#pos-label{pos_num}").text_content()
    assert pos_name, position.inner_html()

    player_stats = zip(
        position.query_selector_all("text.player-name"),
        position.query_selector_all("text.player-stat")
    )
    assert all(pn and ps for (pn, ps) in player_stats)
    return pos_name, player_stats


class TestSummary(BaseTests):
    """
    :py:class:`fangraphs.teams.Summary`.
    """

    address = "https://fangraphs.com/teams/angels"

    @pytest.mark.parametrize(
        "page", ["summary_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.teams.Summary.export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        """
        tables = page.query_selector_all(".team-stats-table")
        assert tables
        assert len(tables) == 2

        assert page.query_selector_all("h2.team-header")
        tnames = [
            e.text_content() for e in page.query_selector_all(
                "h2.team-header"
            )
        ]
        assert all(t for t in tnames)

        for table in tables:
            _test_scrape_data_table(table)

        _test_scrape_depth_chart(page, range(2, 11))
        _test_scrape_depth_chart(page, range(0, 2))


class TestStats(BaseTests):
    """
    :py:class:`fangraphs.teams.Stats`.
    """

    address = "https://fangraphs.com/teams/angels/stats"

    @pytest.mark.parametrize(
        "page", ["stats_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.teams.Stats.test_export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        """
        tables = page.query_selector_all(".team-stats-table")
        assert tables

        tnames = [
            e.text_content() for e in page.query_selector_all(
                "h2.team-header"
            )
        ]
        assert all(t for t in tnames)

        for table in tables:
            _test_scrape_data_table(table)


class TestSchedule(BaseTests):
    """
    :py:class:`fangraphs.teams.Schedule`.
    """

    address = "https://fangraphs.com/teams/angels/schedule"

    @staticmethod
    def _test_get_headers(header_elem):
        """
        :py:meth:`fangraphs.teams.Schedule.get_table_headers`

        :param header_elem:
        :type header_elem: playwright.sync_api._generated.ElementHandle
        """
        assert header_elem.query_selector_all("th")
        headers = [
            e.text_content() for e in header_elem.query_selector_all("th")
        ]
        assert headers

    def _test_scrape_table(self, page):
        """
        :py:meth:`fangraphs.teams.Schedule._scrape_data_table`

        :param page:
        :type page: playwright.sync_api._generated.Page
        :return:
        """
        rows = page.query_selector_all(
            ".team-schedule-table tbody > tr"
        )
        assert rows
        header_elem = rows.pop(0)
        self._test_get_headers(header_elem)

        href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            assert row.query_selector_all("td"), row.inner_html()
            data = [e.text_content() for e in row.query_selector_all("td")]
            assert data, row.inner_html()

            assert len(
                row.query_selector_all("span.date-full")
            ) == 1, (row.inner_html())
            assert len(
                row.query_selector_all("span.date-short")
            ) == 1, (row.inner_html())
            dates = (
                row.query_selector("span.date-full").text_content(),
                row.query_selector("span.date-short").text_content()
            )
            assert dates

            assert len(
                row.query_selector_all("td.alignL:nth-last-child(2)")
            ) == 1, row.inner_html()
            assert len(
                row.query_selector_all("td.alignL:nth-last-child(1)")
            ) == 1, row.inner_html()
            pitchers = (
                row.query_selector("td.alignL:nth-last-child(2)"),
                row.query_selector("td.alignL:nth-last-child(1)")
            )
            assert pitchers

            for elem in pitchers:
                assert len(
                    elem.query_selector_all("a")
                ) == 1, elem.inner_html()
                href = elem.query_selector("a").get_attribute("href")
                assert href, elem.inner_html()
                assert href_regex.search(href), href

    @pytest.mark.parametrize(
        "page", ["schedule_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.teams.Schedule.export`

        :param page: A Playwright ``Page`` object
        :type page: playwright.sync_api._generated.Page
        """
        self._test_scrape_table(page)


class TestPlayerUsage(BaseTests):
    """
    :py:class:`fangraphs.teams.PlayerUsage`.
    """

    address = "https://fangraphs.com/teams/angels/player-usage"

    @staticmethod
    def _test_scrape_table_headers(page):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        elems = page.query_selector_all(".table-scroll thead > tr > th")
        assert elems

        headers = [e.text_content() for e in elems]
        assert all(h for h in headers)

    @staticmethod
    def _test_scrape_table_rows(page):
        """

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        rows = page.query_selector_all(".table-scroll tbody > tr")
        assert rows

        href_regex = re.compile(r"^//www.fangraphs.com/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            assert row.query_selector_all("td")
            data = [e.text_content() for e in row.query_selector_all("td")]
            assert data

            assert len(
                row.query_selector_all(
                    "td[data-stat='Opp SP'] > a"
                )
            ) == 1
            href = row.query_selector(
                "td[data-stat='Opp SP'] > a"
            ).get_attribute("href")
            assert href, row.inner_html()
            assert href_regex.search(href)

    @pytest.mark.parametrize(
        "page", ["playerusage_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.teams.PlayerUsage.export`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        self._test_scrape_table_headers(page)
        self._test_scrape_table_rows(page)


class TestDepthChart(BaseTests):
    """
    :py:class:`fangraphs.teams.DepthChart`.
    """

    address = "https://fangraphs.com/teams/angels/depth-chart"

    @staticmethod
    def _test_get_table_headers(header_elem):
        """
        :py:meth:`fangraphs.teams.DepthChart._get_table_headers`

        :param header_elem:
        :type header_elem: playwright.sync_api._generated.ElementHandle
        """
        assert header_elem.query_selector_all("th")
        headers = [e.text_content() for e in header_elem.query_selector_all("th")]
        assert headers

    def _test_scrape_table(self, table):
        """
        :py:meth:`fangraphs.teams.DepthChart._scrape_data_table`

        :param table:
        :type table: playwright.sync_api._generated.ElementHandle
        """
        rows = table.query_selector_all(".team-stats-table tbody > tr")
        assert rows

        header_elem = rows.pop(0)
        self._test_get_table_headers(header_elem)

        href_regex = re.compile(r"^/statss.aspx\?playerid=(.*)")

        for i, row in enumerate(rows):
            assert row.query_selector_all("td"), row.inner_html()
            data = [e.text_content() for e in row.query_selector_all("td")]
            assert data, row.inner_html()

            try:
                assert len(
                    row.query_selector_all("td.frozen > a")
                ) == 1, row.inner_html()
                href = row.query_selector("td.frozen > a").get_attribute("href")
                assert href_regex.search(href), href
            except AssertionError:
                assert data[0] == "Total", row.inner_html()

    @pytest.mark.parametrize(
        "page", ["depthchart_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.teams.DepthChart.export`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        batting = page.query_selector_all(".team-depth-table-bat")
        assert batting
        pitching = page.query_selector_all(".team-depth-table-pit")
        assert pitching

        for table in batting + pitching:
            assert len(
                table.query_selector_all(
                    ".team-depth-table-pos.team-color-primary"
                )
            ) == 1, table.inner_html()
            tname = table.query_selector(
                ".team-depth-table-pos.team-color-primary"
            ).text_content()
            assert tname

            self._test_scrape_table(table)

        _test_scrape_depth_chart(page, range(2, 11))
        _test_scrape_depth_chart(page, range(0, 2))
