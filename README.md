# FanGraphs-Export

<p align="center">
    <a href="https://fangraphs.com/">
        <img src="https://user-images.githubusercontent.com/72679601/112188979-c335d980-8bc0-11eb-8ab9-992663e9e0e6.png" alt="FanGraphs" width="500" height="250"/></a>
</p>

<p align="center">
    <a href="https://github.com/JLpython-py/FanGraphs-Export/tree/master">
        <img src="https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-export/master" alt="master"/></a>
    <a href="https://github.com/JLpython-py/FanGraphs-Export/tree/development">
        <img src="https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-Export/development" alt="development"/></a>
</p>

<p align="center">
    <a href="https://github.com/JLpython-py/FanGraphs-Export/milestones/1">
        <img src="https://img.shields.io/github/milestones/progress/JLpython-py/FanGraphs-Export/1" alt="Milestone 1"/></a>
    <a href="https://github.com/JLpython-py/FanGraphs-Export/releases">
        <img src="https://img.shields.io/github/v/tag/JLpython-py/FanGraphs-Export" alt="Latest Release"/></a>
    <a href="https://github.com/JLpython-py/FanGraphs-Export">
        <img src="https://img.shields.io/github/license/JLpython-py/FanGraphs-Export" alt="GitHub Repository"/></a>
</p>

FanGraphs is a popular website among the baseball analytic community.
The website is most well-known for its vast coverage of statistics.
The `FanGraphs` package contains various modules for scraping and exporting data from the most popoular of webpages.

## Installation

## Dependencies

- Python >= 3.6
- BeautifulSoup4 4.9.3
- lxml 4.6.3  
- Playwright 1.9.2
- Pytest 6.2.2  
- Requests 2.25.1

To install all the necessary packages, run:

```commandline
pip install -r requirements.txt
```

*Note: Per the [Playwright documentation](https://playwright.dev/python/docs/intro/), the browser binaries must be installed.
To install the browser binaries, run:*

```comandline
playwright install
```

## Documentation

## Basic Usage

Each group of FanGraphs pages (e.g. Leaders, Projections, etc.) which is covered has an individual module.
Each webpage in each group of webpages has an individual class covering the page.

FanGraphs webpage groups:

- [Leaders](#Leaders)

### Leaders

FanGraphs Leaders pages:

- [Major League Leaderboards](https://fangraphs.com/leaders.aspx)
- [Splits Leaderboards](https://fangraphs.com/leaders/splits-leaderboards)
- [Season Stat Grid](https://fangraphs.com/leaders/season-stat-grid)
- [60-Game Span Leaderboards](https://fangraphs.com/leaders/special/game-span)
- [KBO Leaderboards](https://fangraphs.com/leaders/international)
- [WAR Leaderboards](https://fangraphs.com/warleaders.aspx)

```python
from FanGraphs import leaders
mll = leaders.MajorLeagueLeaderboards()
splits = leaders.SplitsLeaderboards()
ssg = leaders.SeasonStatGrid()
gsl = leaders.GameSpanLeaderboards()
intl = leaders.InternationalLeaderboards()
war = leaders.WARLeaderboards()
```

## Tests

To run all tests, run `pytest FanGraphs`

To run the tests for a specific module, run `pytest FanGraphs/test_module_name`.
For example,

```commandline
pytest FanGraphs/test_leaders
```

To run the tests for a specific class, run `pytest -k "TestClassName"`.
For example,

```commandline
pytest -k "TestMajorLeagueLeaderboards"
```

## License

The code in this repository is licensed under an MIT License.

Copyright (c) 2021 Jacob Lee
