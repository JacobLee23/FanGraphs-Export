# FanGraphs-Export

![FanGraphs logo](https://user-images.githubusercontent.com/72679601/112188979-c335d980-8bc0-11eb-8ab9-992663e9e0e6.png)

![Last Commit: master](https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-export/master)
![Last Commit: development](https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-Export/development)

![Milestone 1](https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/1)
![Latest Release](https://img.shields.io/github/v/tag/JLpython-py/FanGraphs-Export)
![License: MIT](https://img.shields.io/github/license/JLpython-py/FanGraphs-Export)
![Read the Docs](https://img.shields.io/readthedocs/fangraphs-export)

The [FanGraphs](https://fangraphs.com/) website, well-known among baseball fans, provides a variety of baseball statistics.
The statistics available are extremely expansive, as the website brags stats for every player in MLB history.

The `fangraphs` package allows for simple, intuitive parsing of the many webpages available.
While not every page is "scrape-able" (i.e. the pages are most composed of graphics),
there are plans for covering as many pages as possible, including the most popular ones.
This package contains modules for scraping and exporting data from each of the covered webpages.

## Dependencies

The `fangraphs` library requires Python version 3.6 or higher.

The following libraries along are required for the `fangraphs` library.

- `BeautifulSoup4`
- `lxml`
- `playwright`
- `pytest`  
- `requests`

*Note: The dependencies of each package listed above are also required.*

To install all the necessary packages, run:

```commandline
pip install -r requirements.txt
```

*Note: The browser binaries of `playwright` are needed for proper usage.
To install the browser binaries, run `playwright install`.
See the [Playwright documentation](https://playwright.dev/python/docs/intro/) for more information.*

## Documentation

The **Read the Docs** documentation can be found [here](https://fangraphs-export.readthedocs.io/en/latest/?).

## Basic Usage

*Note: A more in-depth quickstart is available in the [documentation](#Documentation).*

Each group of FanGraphs pages (e.g. Leaders, Projections, etc.) which is covered has an individual module.
Each webpage in each group of webpages has an individual class covering the page.

Covered FanGraphs webpage groups:

- [Leaders](#Leaders)
- [Projections](#Projections)

### Leaders

FanGraphs Leaders pages:

- [Major League Leaderboards](https://fangraphs.com/leaders.aspx)
- [Splits Leaderboards](https://fangraphs.com/leaders/splits-leaderboards)
- [Season Stat Grid](https://fangraphs.com/leaders/season-stat-grid)
- [60-Game Span Leaderboards](https://fangraphs.com/leaders/special/game-span)
- [KBO Leaderboards](https://fangraphs.com/leaders/international)
- [WAR Leaderboards](https://fangraphs.com/warleaders.aspx)

```python
from fangraphs import leaders

mll = leaders.MajorLeague()
splits = leaders.Splits()
ssg = leaders.SeasonStat()
gsl = leaders.GameSpan()
intl = leaders.International()
war = leaders.WAR()
```

### Projections

FanGraphs Projections pages:

- [Projection Leaderboards](https://fangraphs.com/projections.aspx)

```python
from fangraphs import projections

projl = projections.Projections()
```

## Tests

To run all tests, run `pytest FanGraphs`

To run the tests for a specific module, run `pytest fangraphs/tests/test_module_name.py`.
For example,

```commandline
pytest fangraphs/tests/test_leaders.py
```

To run the tests for a specific class, run `pytest -k "TestClassName"`.
For example,

```commandline
pytest -k "TestMajorLeagueLeaderboards"
```

## License

The code in this repository is licensed under an MIT License.

**Copyright (c) 2021 Jacob Lee**
