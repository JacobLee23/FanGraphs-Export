#! python3
# tests/test_leaders.py

"""
The docstring in each class identifies the class in :py:mod:`fangraphs.leaders` being tested.
The docstring in each test identifies the class attribute(s)/method(s) being tested.
"""

from urllib.request import urlopen

from playwright.sync_api import sync_playwright
import pytest

from fangraphs import leaders
from fangraphs.selectors import leaders_sel


@pytest.fixture(scope="class")
def season_stat_page():
    """
    Pytest fixture which yields a Playwright ``Page`` object, for testing.

    :return: Yields a Playwright ``Page`` object
    :rtype: playwright.sync_api._generated.Page
    """
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page()
        page.goto(leaders.SeasonStat.address, timeout=0)
        page.wait_for_selector(leaders_sel.SeasonStat.waitfor)
        yield page
        browser.close()


@pytest.fixture(scope="class")
def splits_page():
    """
    Pytest fixture which yields a Playwright ``Page`` object, for testing.

    :return: Yields a Playwright ``Page`` object
    :rtype: playwright.sync_api._generated.Page
    """
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page()
        page.goto(leaders.Splits.address, timeout=0)
        page.wait_for_selector(leaders_sel.Splits.waitfor)
        yield page
        browser.close()


class TestGameSpan:
    """
    :py:class:`fangraphs.leaders.GameSpan`
    """

    address = "https://www.fangraphs.com/leaders/special/60-game-span"

    def test_address(self):
        """
        :py:meth:`fangraphs.leaders.GameSpan.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200


class TestInternational:
    """
    :py:class:`fangraphs.leaders.International`
    """

    address = "https://www.fangraphs.com/leaders/international"

    def test_address(self):
        """
        :py:meth:`fangraphs.leaders.International.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200


class TestMajorLeague:
    """
    :py:class:`fangraphs.leaders.MajorLeague`
    """

    address = "https://fangraphs.com/leaders.aspx"

    def test_address(self):
        """
        :py:meth:`fangraphs.leaders.MajorLeague.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200


class TestSeasonStat:
    """
    :py:class:`fangraphs.leaders.SeasonStat`
    """

    address = "https://fangraphs.com/leaders/season-stat-grid"

    def test_address(self):
        """
        :py:meth:`fangraphs.leaders.SeasonStat.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200

    def test_export(self, season_stat_page):
        """
        :py:meth:`fangraphs.leaders.SeasonStat.export`

        :param season_stat_page:
        :type season_stat_page: playwright.sync_api._generated.Page
        """
        assert len(
            season_stat_page.query_selector_all(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            )
        ) == 1
        elem = season_stat_page.query_selector(
            ".table-page-control:nth-last-child(1) > .table-control-total"
        )
        assert elem.text_content()

        self._test_write_table_headers(season_stat_page)
        self._test_write_table_rows(season_stat_page)

        assert len(
            season_stat_page.query_selector_all(
                ".table-page-control:nth-last-child(1) > .next"
            )
        ) == 1

    @staticmethod
    def _test_write_table_headers(page):
        """
        :py:meth:`fangraphs.leaders.SeasonStat._write_table_headers`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        elems = page.query_selector_all(".table-scroll thead tr th")
        assert elems
        assert all(e.text_content() for e in elems)

    @staticmethod
    def _test_write_table_rows(page):
        """
        :py:meth:`fangraphs.leaders.SeasonStat._write_table_rows`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        elems = page.query_selector_all(".table-scroll tbody tr")
        assert elems
        for row in elems:
            subelems = row.query_selector_all("td")
            assert subelems
            assert all(e.text_content() for e in elems)


class TestSplits:
    """
    :py:class:`fangraphs.leaders.Splits`
    """

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    def test_address(self):
        """
        :py:attr:`fangraphs.leaders.Splits.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200

    def test_update(self, splits_page):
        """
        :py:meth:`fangraphs.leaders.Splits.update`

        :param splits_page:
        :type splits_page: playwright.sync_api._generated.Page
        """
        splits_page.click(
            "#stack-buttons .fgButton.small:nth-last-child(1)"
        )
        assert len(
            splits_page.query_selector_all(
                "#button-update"
            )
        ) == 1

    def test_list_filter_groups(self, splits_page):
        """
        :py:meth:`fangraphs.leaders.Splits.list_filter_groups`

        :param splits_page:
        :type splits_page: playwright.sync_api._generated.Page
        """
        elems = splits_page.query_selector_all(
            ".fgBin.splits-bin-controller div"
        )
        assert elems
        assert all(e.text_content() for e in elems)

    def test_set_filter_group(self, splits_page):
        """
        :py:meth:`fangraphs.leaders.Splits.set_filter_group`

        :param splits_page:
        :type splits_page: playwright.sync_api._generated.Page
        """
        elems = splits_page.query_selector_all(
            ".fgBin.splits-bin-controller div"
        )
        assert elems

    def test_reset_filters(self, splits_page):
        """
        :py:meth:`fangraphs.leaders.Splits.reset_filters`

        :param splits_page:
        :type splits_page: playwright.sync_api._generated.Page
        """
        assert len(
            splits_page.query_selector_all(
                "#stack-buttons .fgButton.small:nth-last-child(1)"
            )
        ) == 1


class TestWAR:
    """
    :py:class:`fangraphs.leaders.WAR`
    """

    address = "https://fangraphs.com/warleaders.aspx"

    def test_address(self):
        """
        :py:attr:`fangraphs.leaders.WAR.address`
        """
        res = urlopen(self.address)
        assert res.getcode() == 200
