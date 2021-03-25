#! python3
# FanGraphs/selectors/leaders_sel/international_leaderboards.py

selections = {
    "stat": [
        ".controls-stats > .fgButton:nth-child(1)",
        ".controls-stats > .fgButton:nth-child(2)"
    ],
    "type": [
        ".controls-board-view > .fgButton:nth-child(1)",
        ".controls-board-view > .fgButton:nth-child(2)"
    ]
}
dropdowns = {
    "position": ".controls-stats:nth-child(1) > div:nth-child(3) > .fg-selection-box__selection",
    "min": ".controls-stats:nth-child(1) > div:nth-child(4) > .fg-selection-box__selection",
    "single_season": ".controls-stats:nth-child(2) > div:nth-child(1) > .fg-selection-box__selection",
    "season1": ".controls-stats:nth-child(2) > div:nth-child(2) > .fg-selection-box__selection",
    "season2": ".controls-stats:nth-child(2) > div:nth-child(3) > .fg-selection-box__selection",
    "league": ".controls-stats:nth-child(3) > div:nth-child(1) > .fg-selection-box__selection",
    "team": ".controls-stats:nth-child(3) > div:nth-child(2) > .fg-selection-box__selection",
}
checkboxes = {
    "split_seasons": ".controls-stats > .fg-checkbox"
}
waitfor = ".fg-data-grid.table-type"
