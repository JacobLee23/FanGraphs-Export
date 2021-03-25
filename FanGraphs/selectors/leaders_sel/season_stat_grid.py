#! python3
# FanGraphs/selectors/leaders_sel/season_stat_grid.py

"""
CSS selectors for :py:class:`FanGraphs.leaders.SeasonStatGrid`.
"""

selections = {
    "stat": [
        "div[class*='fgButton button-green']:nth-child(1)",
        "div[class*='fgButton button-green']:nth-child(2)"
    ],
    "type": [
        "div[class*='fgButton button-green']:nth-child(4)",
        "div[class*='fgButton button-green']:nth-child(5)",
        "div[class*='fgButton button-green']:nth-child(6)"
    ]
}
dropdowns = {
    "start_season": ".row-season > div:nth-child(2)",
    "end_season": ".row-season > div:nth-child(4)",
    "popular": ".season-grid-controls-dropdown-row-stats > div:nth-child(1)",
    "standard": ".season-grid-controls-dropdown-row-stats > div:nth-child(2)",
    "advanced": ".season-grid-controls-dropdown-row-stats > div:nth-child(3)",
    "statcast": ".season-grid-controls-dropdown-row-stats > div:nth-child(4)",
    "batted_ball": ".season-grid-controls-dropdown-row-stats > div:nth-child(5)",
    "win_probability": ".season-grid-controls-dropdown-row-stats > div:nth-child(6)",
    "pitch_type": ".season-grid-controls-dropdown-row-stats > div:nth-child(7)",
    "plate_discipline": ".season-grid-controls-dropdown-row-stats > div:nth-child(8)",
    "value": ".season-grid-controls-dropdown-row-stats > div:nth-child(9)"
}
waitfor = ".fg-data-grid.undefined"
