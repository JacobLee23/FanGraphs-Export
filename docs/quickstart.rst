Fangraphs Quickstart
====================

ScrapingUtilities
-----------------

All scraper objects inherit ``fangraphs.ScrapingUtilities``.

All the classes share a few methods which perform the same tasks:

- `list_queries(self)`: Lists the usable filter queries of the page
- `list_options(self, query)`: Lists the options which ``query`` can be configured to
- `current_option(self, query)`: Returns the current option which ``query`` is configured to
- `configure(self, query, option)`: Configures ``query`` to ``option``.

Since each class inherits the same parent class,
the following methods inherited from ``fangraphs.ScrapingUtilities`` are also available to each class:

- `export(self)`: Export the current data table, returning the data in a ``pandas.DataFrame`` object.
- `reset(self)`: Navigates the remote browser to the original webpage.

Pages
-----

Each webpages which can be scraped has its own web scraper class.
The module where the class belongs depends on the group the webpage is in.
The class depends on the webpage itself.

+---------------------------+-----------------------------------+
| FanGraphs webpage group   | :py:mod:`fangraphs` Module        |
+===========================+===================================+
| Leaders                   | :py:mod:`fangraphs.leaders`       |
+---------------------------+-----------------------------------+
| Projections               | :py:mod:`fangraphs.projections`   |
+---------------------------+-----------------------------------+
| Depth Charts              | :py:mod:`fangraphs.depth_charts`  |
+---------------------------+-----------------------------------+
| Teams                     | :py:mod:`fangraphs.teams`         |
+---------------------------+-----------------------------------+

Leaders
^^^^^^^

FanGraphs webpages under the **Leaders** tab.

+-------------------------------+-------------------------------------------+
| FanGraphs **Leaders** page    | :py:mod:`fangraphs.leaders` class         |
+===============================+===========================================+
| `60-Game Span Leaderboards`_  | :py:mod:`fangraphs.leaders.GameSpan`      |
+-------------------------------+-------------------------------------------+
| `KBO Leaders`_                | :py:mod:`fangraphs.leaders.International` |
+-------------------------------+-------------------------------------------+
| `Major League Leaders`_       | :py:mod:`fangraphs.leaders.MajorLeague`   |
+-------------------------------+-------------------------------------------+
| `Season Stat Grid`_           | :py:mod:`fangraphs.leaders.SeasonStat`    |
+-------------------------------+-------------------------------------------+
| `Splits Leaderboards`_        | :py:mod:`fangraphs.leaders.Splits`        |
+-------------------------------+-------------------------------------------+
| `Combined WAR Leaderboards`_  | :py:mod:`fangraphs.leaders.WAR`           |
+-------------------------------+-------------------------------------------+

.. _60-Game Span Leaderboards: https://fangraphs.com/leaders/special/game-span
.. _KBO Leaders: https://fangraphs.com/leaders/international
.. _Major League Leaders: https://fangraphs.com/leaders.aspx
.. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
.. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
.. _Combined WAR Leaderboards: https://fangraphs.com/warleaders.aspx


Projections
^^^^^^^^^^^

FanGraphs webpages under the **Projections** tab.

+-----------------------------------+-----------------------------------------------+
| FanGraphs **Projections** page    | :py:mod:`fangraphs.projections` class         |
+===================================+===============================================+
| `Projections Leaderboards`_       | :py:class:`fangraphs.projections.Projections` |
+-----------------------------------+-----------------------------------------------+

Note: The **Projections Leaderboards** page includes all **Projections** pages under the following subcategories:

- Pre-Season Projections
- 600 PA / 200 IP Projections
- Updated In-Season Projections
- 3 Year Projections

.. _Projections Leaderboards: https://fangraphs.com/projections.aspx


Depth Charts
^^^^^^^^^^^^

FanGraphs depth chart pages under the **Teams** tab.

+-----------------------------------+-----------------------------------------------+
| FanGraphs **Depth Charts** page   | :py:mod:`fangraphs.depth_charts` class        |
+===================================+===============================================+
| `Team WAR Totals`_                | :py:mod:`fangraphs.depth_charts.DepthCharts`  |
+-----------------------------------+-----------------------------------------------+
| `Team Depth Charts`_              | :py:mod:`fangraphs.depth_charts.DepthCharts`  |
+-----------------------------------+-----------------------------------------------+
| `Positional Depth Charts`_        | :py:mod:`fangraphs.depth_charts.DepthCharts`  |
+-----------------------------------+-----------------------------------------------+

.. _Team WAR Totals: https://www.fangraphs.com/depthcharts.aspx?position=Team
.. _Team Depth Charts: https://www.fangraphs.com/depthcharts.aspx?position=ALL&teamid=1
.. _Positional Depth Charts: https://www.fangraphs.com/depthcharts.aspx?position=C


Teams
^^^^^

FanGraphs team pages under the **Teams** tab.

+---------------------------+-------------------------------------------+
| FanGraphs **Teams** page  | :py:mod:`fangraphs.teams` class           |
+===========================+===========================================+
| `Summary`_                | :py:class:`fangraphs.teams.Summary`       |
+---------------------------+-------------------------------------------+
| `Stats`_                  | :py:class:`fangraphs.teams.Stats`         |
+---------------------------+-------------------------------------------+
| `Schedule`_               | :py:class:`fangraphs.teams.Schedule`      |
+---------------------------+-------------------------------------------+
| `Player Usage`_           | :py:class:`fangraphs.teams.PlayerUsage`   |
+---------------------------+-------------------------------------------+
| `Depth Chart`_            | :py:class:`fangraphs.teams.DepthChart`    |
+---------------------------+-------------------------------------------+

.. _Summary: https://fangraphs.com/teams/angels/
.. _Stats: https://fangraphs.com/teams/angels/stats/
.. _Schedule: https://fangraphs.com/teams/angels/schedule/
.. _Player Usage: https://fangraphs.com/teams/angels/player-usage/
.. _Depth Chart: https://fangraphs.com/teams/angels/depth-chart/


Basic Usage
-----------

A scraper object can be created to scrape the corresponding webpage by calling the class.
The only required argument is ``browser``, which must be a Playwright ``Browser`` object.
This argument can be passed by nesting the call in the context manager.

.. code-block:: python

    from playwright.sync_api import sync_playwright
    from fangraphs.leaders import MajorLeague

    with sync_playwright() as play:
        browser_type = play.chromium    # OR play.firefox OR play.webkit
        browser = browser_type.launch(
            accept_downloads=True
        )
        scraper = MajorLeague(browser)
        # Do stuff with 'scraper'
        browser.close()

Alternatively, the :py:func:`fangraphs.fangraphs_scraper` function decorator can be used.
Using the function decorator is recommended, as it allows for the simple reuse of the decorated function.

.. code-block:: python

    from fangraphs import fangraphs_scraper
    from fangraphs.leaders import MajorLeague

    @fangraphs_scraper
    def scrape_leaderboard(scraper):
        # Do stuff with 'scraper'

    scrape_leaderboards(MajorLeague)

Leaders
^^^^^^^

.. code-block:: python

    from fangraphs import fangraphs_scraper
    from fangraphs import leaders

    @fangraphs_scraper
    def scrape_leaderboard(scraper):
        pass

    scrape_leaderboard(leaders.GameSpan)
    scrape_leaderboard(leaders.International)
    scrape_leaderboard(leaders.MajorLeague)
    scrape_leaderboard(leaders.SeasonStat)
    scrape_leaderboard(leaders.Splits)
    scrape_leaderboard(leaders.WAR)

Projections
^^^^^^^^^^^

.. code-block:: python

    from fangraphs import fangraphs_scraper
    from fangraphs import projections

    @fangraphs_scraper
    def scrape_leaderboard(scraper):
        pass

    scrape_leaderboard(projections.Projections)

Teams
^^^^^

.. code-block:: python

    from fangraphs import fangraphs_scraper
    from fangraphs import teams

    @fangraphs_scraper
    def scrape_leaderboard(scraper):
        pass

    scrape_leaderboard(teams.DepthCharts)

Example Usage
-------------

Below is a basic example with a ``MajorLeague`` object:

.. code-block:: python

    from fangraphs import fangraphs_scraper
    from fangraphs import leaders

    @fangraphs_scraper
    def get_dodgers_pitching(scraper):
        scraper.configure("stat", "Pitching")
        scraper.configure("team", "LAD")
        dataframe = scraper.export()
        return dataframe

    df = get_dodgers_pitching(leaders.MajorLeague)
