#! python3
# FanGraphs/leaders/__init__.py

"""
Scrapers for the webpages under the FanGaphs **Leaders** tab.
"""

import csv
import datetime
import os

import fangraphs.exceptions
from fangraphs import ScrapingUtilities
from fangraphs.selectors import leaders_sel


class GameSpan(ScrapingUtilities):
    """
    Scraper for the FanGraphs `60-Game Span Leaderboards`_ page.

    .. _60-Game Span Leaderboards: https://www.fangraphs.com/leaders/special/60-game-span
    """

    address = "https://fangraphs.com/leaders/special/60-game-span"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.GameSpan)
        self.queries = leaders_sel.GameSpan(self.page)


class International(ScrapingUtilities):
    """
    Scraper for the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """

    address = "https://www.fangraphs.com/leaders/international"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.International)
        self.queries = leaders_sel.International(self.page)


class MajorLeague(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Major League Leaderboards`_ page.

    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`.

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """

    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.MajorLeague)
        self.queries = leaders_sel.MajorLeague(self.page)


class SeasonStat(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Season Stat Grid`_ page.

    .. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
    """

    address = "https://fangraphs.com/leaders/season-stat-grid"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.SeasonStat)
        self.queries = leaders_sel.SeasonStat(self.page)

    @staticmethod
    def _write_table_headers(page, writer: csv.writer):
        """
        Writes the headers of the data table to the CSV file.

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param writer: The ``csv.writer`` object
        """
        elems = page.query_selector_all(".table-scroll thead tr th")
        headers = [e.text_content() for e in elems]
        writer.writerow(headers)

    @staticmethod
    def _write_table_rows(page, writer: csv.writer):
        """
        Iterates through the rows of the current data table.
        The data in each row is written to the CSV file.

        :param page:
        :type page: playwright.sync_api._generated.Page
        :param writer: The ``csv.writer`` object
        """
        row_elems = page.query_selector_all(".table-scroll tbody tr")
        for row in row_elems:
            elems = row.query_selector_all("td")
            items = [e.text_content() for e in elems]
            writer.writerow(items)

    def export(self, path):
        """
        Scrapes and saves the data from the table of the current leaderboards.
        The data will be exported as a CSV file and the file will be saved to *out/*.
        The file will be saved to the filepath ``path``, if specified.
        Otherwise, the file will be saved to the filepath *out/%d.%m.%y %H.%M.%S.csv*.

        *Note: This is a 'manual' export of the data.
        In other words, the data is scraped from the table.
        This is unlike other forms of export where a button is clicked.
        Thus, there will be no record of a download when the data is exported.*

        :param path: The path to save the exported file to
        """
        self._close_ad()
        if not path or os.path.splitext(path)[1] != ".csv":
            path = "out/{}.csv".format(
                datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
            )
        total_pages = int(
            self.page.query_selector(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            ).text_content()
        )
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            self._write_table_headers(self.page, writer)
            for _ in range(0, total_pages):
                self._write_table_rows(self.page, writer)
                self.page.click(
                    ".table-page-control:nth-last-child(1) > .next"
                )


class Splits(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Splits Leaderboards`_ page.

    .. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
    """

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.Splits)
        self.queries = leaders_sel.Splits(self.page)
        self.qsbatting = leaders_sel.QuickSplits.Batting()
        self.qspitching = leaders_sel.QuickSplits.Pitching()

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapability: No filter queries to update
        """
        elem = self.page.query_selector("#button-update")
        if elem is None:
            raise fangraphs.exceptions.FilterUpdateIncapability()
        self._close_ad()
        elem.click()

    def list_filter_groups(self):
        """
        Lists the possible groups of filter queries which can be used

        :return: Names of the groups of filter queries
        :rtype: list
        """
        elems = self.page.query_selector_all(".fgBin.splits-bin-controller div")
        groups = [e.text_content() for e in elems]
        return groups

    def set_filter_group(self, group="Show All"):
        """
        Configures the available filters to a specified group of filters

        :param group: The name of the group of filters
        """
        options = [o.lower() for o in self.list_filter_groups()]
        try:
            index = options.index(group)
        except ValueError as err:
            raise fangraphs.exceptions.InvalidFilterGroup(group) from err
        self._close_ad()
        elem = self.page.query_selector_all(
            ".fgBin.splits-bin-controller div"
        )[index]
        elem.click()

    def reset_filters(self):
        """
        Resets filters to the original option(s).
        This does not affect the following filter queries:

        - ``group``
        - ``stat``
        - ``type``
        - ``groupby``
        - ``preset_range``
        - ``auto_pt``
        - ``split_teams``
        """
        elem = self.page.query_selector(
            "#stack-buttons .fgButton.small:nth-last-child(1)"
        )
        if elem is None:
            return
        self._close_ad()
        elem.click()

    def list_quick_splits(self):
        """
        Lists all the quick splits which can be used.
        Quick splits allow for the configuration of multiple filter queries at once.

        :return: All available quick splits
        :rtype: list
        """
        quick_splits = []
        quick_splits.extend(list(self.qsbatting.__dict__))
        quick_splits.extend(list(self.qspitching.__dict__))
        return quick_splits

    def set_to_quick_split(self, quick_split_selector: str, autoupdate=True):
        """
        Invokes the configuration of a quick split.
        All filter queries affected by :py:meth:`reset_filters` are reset prior to configuration.
        This action is performed by the FanGraphs API and cannot be prevented.

        The selectors which can be passed as ``quick_split_selector`` are stored as attributes of ``self``.
        The batting quick splits are in :py:attr:`qsbatting`.
        The pitching quick splits are in :py:attr:`qspitching`.
        For example, to configure to **Batting: Home**, call ``self.set_to_quick_split(self.qsbatting.home)``.

        :param quick_split_selector: The CSS selector which corresponds to the quick split
        :param autoupdate: If ``True``, :py:meth:`reset_filters` will be called
        :raises FanGraphs.exceptions.InvalidQuickSplits: Invalid argument ``quick_split``
        """
        self.page.click(quick_split_selector)
        if autoupdate:
            self.update()


class WAR(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Combined WAR Leaderboards`_ page.

    .. _Combined WAR Leaderboards: https://www.fangraphs.com/warleaders.aspx
    """

    address = "https://fangraphs.com/warleaders.aspx"

    def __init__(self, browser):
        ScrapingUtilities.__init__(self, browser, self.address, leaders_sel.WAR)
        self.queries = leaders_sel.WAR(self.page)
