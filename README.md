# FanGraphs-Export

![FanGraphs logo](https://user-images.githubusercontent.com/72679601/112188979-c335d980-8bc0-11eb-8ab9-992663e9e0e6.png)

![Last Commit: master](https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-export/master)
![Last Commit: development](https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-Export/development)

![GitHub milestones](https://img.shields.io/github/milestones/all/JLpython-py/FanGraphs-Export)
![Milestone 1](https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/1)
![Milestone 2](https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/2)
![Milestone 3](https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/3)
![Milestone 4](https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/4)

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

- `pandas`
- `playwright`
- `pytest`

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
- [Depth Charts](#Depth-Charts)
- [Teams](#Teams)

### Leaders

FanGraphs Leaders pages:

- [Major League Leaderboards](https://fangraphs.com/leaders.aspx)
- [Splits Leaderboards](https://fangraphs.com/leaders/splits-leaderboards)
- [Season Stat Grid](https://fangraphs.com/leaders/season-stat-grid)
- [60-Game Span Leaderboards](https://fangraphs.com/leaders/special/game-span)
- [KBO Leaderboards](https://fangraphs.com/leaders/international)
- [WAR Leaderboards](https://fangraphs.com/warleaders.aspx)

```python
from fangraphs import fangraphs_scraper
from fangraphs.leaders import *

@fangraphs_scraper
def scrape_page(scraper):
    return scraper.export()

mll = scrape_page(MajorLeague)
splits = scrape_page(Splits)
ssg = scrape_page(SeasonStat)
gsl = scrape_page(GameSpan)
intl = scrape_page(International)
war = scrape_page(WAR)
```

### Projections

FanGraphs Projections pages:

- [Projection Leaderboards](https://fangraphs.com/projections.aspx)

```python
from fangraphs import fangraphs_scraper
from fangraphs.projections import *

@fangraphs_scraper
def scrape_page(scraper):
    return scraper.export()

projl = scrape_page(Projections)
```

### Depth Charts

FanGraphs Depth Charts pages:

- [Depth Charts](https://fangraphs.com/depthcharts.aspx)

```python
from fangraphs import fangraphs_scraper
from fangraphs.depth_charts import *

@fangraphs_scraper
def scrape_page(scraper):
    return scraper.export()

scrape_page(DepthCharts)
```

### Teams

FanGraphs Teams pages:

- [Summary](https://fangraphs.com/teams/angels)
- [Stats](https://fangraphs.com/teams/angels/stats)
- [Schedule](https://fangraphs.com/team/angels/schedule)
- [Player Usage](https://fangraphs.com/teams/angels/player-usage)
- [Depth Chart](https://fangraphs.com/teams/angels/depth-chart)

```python
from fangraphs import fangraphs_scraper
from fangraphs.teams import *

@fangraphs_scraper
def scrape_page(scraper):
    return scraper.export()

summary = scrape_page(Summary)
stats = scrape_page(Stats)
schedule = scrape_page(Schedule)
player_usage = scrape_page(PlayerUsage)
depth_chart = scrape_page(DepthChart)
```

## Tests

To run all tests, run `pytest FanGraphs`

To run the tests for a specific module, run `pytest fangraphs/tests/test_"module name".py`.
For example,

```commandline
pytest fangraphs/tests/test_leaders.py
```

To run the tests for a specific class, run `pytest -k "TestClassName"`.
For example,

```commandline
pytest -k "TestMajorLeague"
```

## License

The code in this repository is licensed under an MIT License.

**Copyright (c) 2021 Jacob Lee**
