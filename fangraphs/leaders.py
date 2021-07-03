#! usr/bin/env python
# fangraphs/leaders.py

"""
Scrapers for the webpages under the FanGaphs **Leaders** tab.
"""

import pandas as pd

import fangraphs.exceptions
from fangraphs import ScrapingUtilities
from fangraphs.selectors import leaders_


class GameSpan(ScrapingUtilities):
    """
    Scraper for the FanGraphs `60-Game Span Leaderboards`_ page.

    .. _60-Game Span Leaderboards: https://www.fangraphs.com/leaders/special/60-game-span
    """

    address = "https://fangraphs.com/leaders/special/60-game-span"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.GameSpan)


class International(ScrapingUtilities):
    """
    Scraper for the FanGraphs `KBO Leaderboards`_ page.

    .. _KBO Leaderboards: https://www.fangraphs.com/leaders/international
    """

    address = "https://www.fangraphs.com/leaders/international"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser

        .. py:attribute:: browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.International)


class MajorLeague(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Major League Leaderboards`_ page.

    Note that the Splits Leaderboard is not covered.
    Instead, it is covered by :py:class:`SplitsLeaderboards`.

    .. _Major League Leaderboards: https://fangraphs.com/leaders.aspx
    """

    address = "https://fangraphs.com/leaders.aspx"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser

        .. py:attribute:: browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.MajorLeague)


class SeasonStat(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Season Stat Grid`_ page.

    .. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
    """

    address = "https://fangraphs.com/leaders/season-stat-grid"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.SeasonStat)

    def _write_table_headers(self):
        """
        Initializes a new DataFrame with columns corresponding to the table headers.

        :return: A DataFrame with columns set to the table headers
        :rtype: pandas.DataFrame
        """
        elems = self.page.query_selector_all(".table-scroll thead tr th")
        headers = [e.text_content() for e in elems]
        dataframe = pd.DataFrame(columns=headers[1:])
        return dataframe

    def _write_table_rows(self, dataframe):
        """
        Writes the data from each of the rows of each of the tables to the DataFrame.

        :param dataframe: The DataFrame to modify
        :type dataframe: pandas.DataFrame
        :return: The DataFrame updated with all the table leaderboard data
        :rtype: pandas.DataFrame
        """
        total_pages = int(
            self.page.query_selector(
                ".table-page-control:nth-last-child(1) > .table-control-total"
            ).text_content()
        )
        index = 0
        for page in range(total_pages):
            row_elems = self.page.query_selector_all(".table-scroll tbody tr")
            for i, row in enumerate(row_elems):
                elems = row.query_selector_all("td")
                items = [e.text_content() for e in elems]
                dataframe.loc[index+i] = items[1:]
            index += len(row_elems)
            self.page.click(".table-page-control:nth-last-child(1) > .next")
        return dataframe

    def export(self):
        """
        Exports the data in the current leaderboard as a DataFrame.

        :return: A DataFrame containing the table data
        :rtype: pandas.DataFrame
        """
        self._close_ad()

        dataframe = self._write_table_headers()
        dataframe = self._write_table_rows(dataframe)

        return dataframe


class Splits(ScrapingUtilities):
    """
    Scraper for the FanGraphs `Splits Leaderboards`_ page.

    .. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
    """

    address = "https://fangraphs.com/leaders/splits-leaderboards"

    def __init__(self, browser):
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser

        .. py:attribute:: qsbatting

            Contains the CSS selectors for the batting-related quick splits.
            Allows for the configuration of the Splits leaderboard to any batting quick split.

            :type: fangraphs.leaders_sel.QuickSplits.Batting

        .. py:attribute:: qspitching

            Contains the CSS selectors for the pitching-related quick splits.
            Allows for the configuration of the Splits leaderboard to any pitching quick split.

            :type: fangraphs.leaders_sel.QuickSplits.Pitching
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.Splits)
        self.qsbatting = leaders_.QuickSplits.Batting()
        self.qspitching = leaders_.QuickSplits.Pitching()

    def update(self):
        """
        Clicks the **Update** button of the page.
        All configured filters are submitted and the page is refreshed.

        :raises FanGraphs.exceptions.FilterUpdateIncapability: No filter queries to update
        :rtype: None
        """
        elem = self.page.query_selector("#button-update")
        if elem is None:
            raise fangraphs.exceptions.FilterUpdateIncapability()
        self._close_ad()
        elem.click()

    def list_filter_groups(self):
        """
        Lists the possible groups of filter queries which can be used.

        :return: Names of the groups of filter queries
        :rtype: list[str]
        """
        elems = self.page.query_selector_all(".fgBin.splits-bin-controller div")
        groups = [e.text_content() for e in elems]
        return groups

    def set_filter_group(self, group="Show All"):
        """
        Configures the available filters to a specified group of filters.

        :param group: The name of the group of filters
        :rtype: None
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

        :rypte: None
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
        :rtype: list[str]
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
        :rtype: None
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
        """
        :param browser: A Playwright ``Browser`` object
        :type browser: playwright.sync_api._generated.Browser
        """
        ScrapingUtilities.__init__(self, browser, self.address, leaders_.WAR)
