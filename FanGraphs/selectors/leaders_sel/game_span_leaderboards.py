#! python3
# FanGraphs/selectors/leaders_sel.game_span_leaderboards.py

selections = {
    "stat": [
        ".controls-stats > .fgButton:nth-child(1)",
        ".controls-stats > .fgButton:nth-child(2)"
    ],
    "type": [
        ".controls-board-view > .fgButton:nth-child(1)",
        ".controls-board-view > .fgButton:nth-child(2)",
        ".controls-board-view > .fgButton:nth-child(3)"
    ]
}
dropdowns = {
    "min_pa": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
    "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
    "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
    "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
    "determine": ".controls-stats.stat-determined > div:nth-child(1) > .fg-selection-box__selection"
}