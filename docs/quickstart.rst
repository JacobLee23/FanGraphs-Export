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

- `export(self, *, path)`: Export the current data table as a CSV file, to ``path``.
- `reset(self)`: Navigates the remote browser to the original webpage.
- `quit(self)`: Terminates the remote browser.

Pages
-----

Each webpages which can be scraped has its own web scraper class.
The module where the class belongs depends on the group the webpage is in.
The class depends on the webpage itself.

+---------------------------+-------------------------------+
| FanGraphs webpage group   | ``fangraphs`` package         |
+===========================+===============================+
| Leaders                   | ``fangraphs.leaders``         |
+---------------------------+-------------------------------+
| Projections               | ``fangraphs.projections``     |
+---------------------------+-------------------------------+
| Depth Charts              | ``fangraphs.depth_charts``    |
+---------------------------+-------------------------------+

Leaders
^^^^^^^

FanGraphs webpages under the **Leaders** tab.

+-------------------------------+---------------------------------------+
| FanGraphs **Leaders** page    | ``fangraphs.leaders`` class           |
+===============================+=======================================+
| `60-Game Span Leaderboards`_  | ``fangraphs.leaders.GameSpan``        |
+-------------------------------+---------------------------------------+
| `KBO Leaders`_                | ``fangraphs.leaders.International``   |
+-------------------------------+---------------------------------------+
| `Major League Leaders`_       | ``fangraphs.leaders.MajorLeague``     |
+-------------------------------+---------------------------------------+
| `Season Stat Grid`_           | ``fangraphs.leaders.SeasonStat``      |
+-------------------------------+---------------------------------------+
| `Splits Leaderboards`_        | ``fangraphs.leaders.Splits``          |
+-------------------------------+---------------------------------------+
| `Combined WAR Leaderboards`_  | ``fangraphs.leaders.WAR``             |
+-------------------------------+---------------------------------------+

.. _60-Game Span Leaderboards: https://fangraphs.com/leaders/special/game-span
.. _KBO Leaders: https://fangraphs.com/leaders/international
.. _Major League Leaders: https://fangraphs.com/leaders.aspx
.. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
.. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
.. _Combined WAR Leaderboards: https://fangraphs.com/warleaders.aspx


Projections
^^^^^^^^^^^

FanGraphs webpages under the **Projections** tab.

+-----------------------------------+---------------------------------------+
| FanGraphs **Projections** page    | ``fangraphs.projections`` class       |
+===================================+=======================================+
| `Projections Leaderboards`_       | ``fangraphs.projections.Projections`` |
+-----------------------------------+---------------------------------------+

Note: The **Projections Leaderboards** page includes all **Projections** pages under the following subcategories:

- Pre-Season Projections
- 600 PA / 200 IP Projections
- Updated In-Season Projections
- 3 Year Projections

.. _Projections Leaderboards: https://fangraphs.com/projections.aspx


Teams
^^^^^

FanGraphs webpages under the **Teams** tab.

+-------------------------------+-----------------------------------+
| FanGraphs **Teams** page      | ``fangraphs.teams`` class         |
+===============================+===================================+
| `Team WAR Totals`_            | ``fangraphs.teams.DepthCharts``   |
+-------------------------------+-----------------------------------+
| `Team Depth Charts`_          | ``fangraphs.teams.DepthCharts``   |
+-------------------------------+-----------------------------------+
| `Positional Depth Charts`_    | ``fangraphs.teams.DepthCharts``   |
+-------------------------------+-----------------------------------+

.. _Team WAR Totals: https://www.fangraphs.com/depthcharts.aspx?position=Team
.. _Team Depth Charts: https://www.fangraphs.com/depthcharts.aspx?position=ALL&teamid=1
.. _Positional Depth Charts: https://www.fangraphs.com/depthcharts.aspx?position=C

Basic Usage
-----------

An object can be created to scrape the corresponding webpage by calling the class, with no arguments.

Leaders
^^^^^^^

.. code-block:: python

    from fangraphs import leaders

    gsl = leaders.GameSpan()
    inter = leaders.International()
    mll = leaders.MajorLeague()
    ssg = leaders.SeasonStat()
    splitsl = leaders.Splits()
    warl = leaders.WAR()

Projections
^^^^^^^^^^^

.. code-block:: python

    from fangraphs import projections
    proj = projections.Projections()

Teams
^^^^^

.. code-block:: python

    from fangraphs import teams
    teamsl = teams.DepthCharts()

Alternatively, the classes can be used as context managers:

.. code-block:: python

    from fangraphs import leaders
    from fangraphs import projections
    from fangraphs import teams

    with leaders.ScraperClass() as scraper:
        # Do stuff here

    with projections.ScraperClass() as scraper:
        # Do stuff here

    with teams.ScraperClass() as scraper:
        # Do stuff here

Example Usage
-------------

Below is a basic example with a ``MajorLeague`` object:

.. code-block:: python

    from fangraphs import leaders
    scraper = leaders.MajorLeague()
    scraper.configure("stat", "Pitching")
    scraper.configure("team", "LAD")
    scraper.export(path="LADPitching.csv")
    scraper.quit()

Or, using the context manager syntax:

.. code-block:: python

    from fangraphs import leaders
    with leaders.MajorLeague() as scraper:
        scraper.configure("stat", "Pitching")
        scraper.configure("team", "LAD")
        scraper.export(path="LADPitching.csv")
