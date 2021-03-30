Fangraphs Quickstart
====================

Leaders
-------

Pages
^^^^^

The webpages under the FanGraphs **Leaders** tab are covered by the ``fangraphs.leaders`` package.
Each page has its own web scraper class in the ``fangraphs.leaders.leaders`` module.
Each covered FanGraphs **Leaders** page with the corresponding class is listed below:

+-------------------------------+-----------------------------------------------+
| FanGraphs Leaders page        | ``fangraphs`` class                           |
+===============================+===============================================+
| `60-Game Span Leaderboards`_  | ``fangraphs.leaders.leaders.GameSpan``        |
+-------------------------------+-----------------------------------------------+
| `KBO Leaders`_                | ``fangraphs.leaders.leaders.International``   |
+-------------------------------+-----------------------------------------------+
| `Major League Leaders`_       | ``fangraphs.leaders.leaders.MajorLeague``     |
+-------------------------------+-----------------------------------------------+
| `Season Stat Grid`_           | ``fangraphs.leaders.leaders.SeasonStat``      |
+-------------------------------+-----------------------------------------------+
| `Splits Leaderboards`_        | ``fangraphs.leaders.leaders.Splits``          |
+-------------------------------+-----------------------------------------------+
| `Combined WAR Leaderboards`_  | ``fangraphs.leaders.leaders.WAR``             |
+-------------------------------+-----------------------------------------------+

.. _60-Game Span Leaderboards: https://fangraphs.com/leaders/special/game-span
.. _KBO Leaders: https://fangraphs.com/leaders/international
.. _Major League Leaders: https://fangraphs.com/leaders.aspx
.. _Season Stat Grid: https://fangraphs.com/leaders/season-stat-grid
.. _Splits Leaderboards: https://fangraphs.com/leaders/splits-leaderboards
.. _Combined WAR Leaderboards: https://fangraphs.com/warleaders.aspx

Usage Introduction
^^^^^^^^^^^^^^^^^^

An object can be created to scrape the corresponding webpage by calling the class, with not arguments::

    from fangraphs.leaders import leaders

    gsl = leaders.GameSpan()
    inter = leaders.International()
    mll = leaders.MajorLeague()
    ssg = leaders.SeasonStat()
    splitsl = leaders.Splits()
    warl = leaders.WAR()

Alternatively, the classes can be used as context managers::

    from fangraphs.leaders import leaders

    with leaders.MajorLeague() as scraper:
        # Do stuff here

Basic Usage
^^^^^^^^^^^

All the classes share a few methods which perform the same tasks:

- `list_queries(self)`: Lists the usable filter queries of the page
- `list_options(self, query)`: Lists the options which ``query`` can be configured to
- `current_option(self, query)`: Returns the current option which ``query`` is configured to
- `configure(self, query, option)`: Configures ``query`` to ``option``.
- `export(self, path="")`: Exports the current data table as a CSV file, to ``path``.

Since each class inherits the same parent class, the following methods are also available:

- `reset(self)`: Navigates the remote browser to the original webpage.
- `quit(self)`: Terminates the remote browser.

Below is a basic example with a ``MajorLeague`` object::

    from fangraphs.leaders import leaders
    scraper = leaders.MajorLeague()
    scraper.configure("stat", "Pitching")
    scraper.configure("team", "LAD")
    scraper.export("LADPitching.csv")
    scraper.quit()

Or, using the context manager syntax::

    from fangraphs.leaders import leaders
    with leaders.MajorLeague() as scraper:
        scraper.configure("stat", "Pitching")
        scraper.configure("team", "LAD")
        scraper.export("LADPitching.csv")

