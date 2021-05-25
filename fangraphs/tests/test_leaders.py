#! python3
# tests/test_leaders.py

"""
Unit tests for :py:mod:`fangraphs.leaders`.
"""

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
def season_stat_page():
    return TestSeasonStat.address


@pytest.fixture(scope="module")
def splits_page():
    return TestSplits.address


class TestGameSpan(BaseTests):
    """
    :py:class:`fangraphs.leaders.GameSpan`
    """

    address = "https://www.fangraphs.com/leaders/special/60-game-span"


class TestInternational(BaseTests):
    """
    :py:class:`fangraphs.leaders.International`
    """

    address = "https://www.fangraphs.com/leaders/international"


class TestMajorLeague(BaseTests):
    """
    :py:class:`fangraphs.leaders.MajorLeague`
    """

    address = "https://fangraphs.com/leaders.aspx"


class TestSeasonStat(BaseTests):
    """
    :py:class:`fangraphs.leaders.SeasonStat`
    """

    address = "https://fangraphs.com/leaders/season-stat-grid"

    @pytest.mark.parametrize(
        "page", ["season_stat_page"], indirect=True
    )
    def test_export(self, page):
        """
        :py:meth:`fangraphs.leaders.SeasonStat.export`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        assert len(
            page.query_selector_all(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            )
        ) == 1
        elem = page.query_selector(
            ".table-page-control:nth-last-child(1) > .table-control-total"
        )
        assert elem.text_content()

        self._test_write_table_headers(page)
        self._test_write_table_rows(page)

        assert len(
            page.query_selector_all(
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


class TestSplits(BaseTests):
    """
    :py:class:`fangraphs.leaders.Splits`
    """

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    @pytest.mark.parametrize(
        "page", ["splits_page"], indirect=True
    )
    def test_update(self, page):
        """
        :py:meth:`fangraphs.leaders.Splits.update`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        page.click(
            "#stack-buttons .fgButton.small:nth-last-child(1)"
        )
        assert len(
            page.query_selector_all(
                "#button-update"
            )
        ) == 1

    @pytest.mark.parametrize(
        "page", ["splits_page"], indirect=True
    )
    def test_list_filter_groups(self, page):
        """
        :py:meth:`fangraphs.leaders.Splits.list_filter_groups`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        elems = page.query_selector_all(
            ".fgBin.splits-bin-controller div"
        )
        assert elems
        assert all(e.text_content() for e in elems)

    @pytest.mark.parametrize(
        "page", ["splits_page"], indirect=True
    )
    def test_set_filter_group(self, page):
        """
        :py:meth:`fangraphs.leaders.Splits.set_filter_group`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        elems = page.query_selector_all(
            ".fgBin.splits-bin-controller div"
        )
        assert elems

    @pytest.mark.parametrize(
        "page", ["splits_page"], indirect=True
    )
    def test_reset_filters(self, page):
        """
        :py:meth:`fangraphs.leaders.Splits.reset_filters`

        :param page:
        :type page: playwright.sync_api._generated.Page
        """
        assert len(
            page.query_selector_all(
                "#stack-buttons .fgButton.small:nth-last-child(1)"
            )
        ) == 1


class TestWAR(BaseTests):
    """
    :py:class:`fangraphs.leaders.WAR`
    """

    address = "https://fangraphs.com/warleaders.aspx"
