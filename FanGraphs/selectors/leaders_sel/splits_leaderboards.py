#! python3
# FanGraphs/selectors/leaders_sel/splits_leaderboards.py

selections = {
    "group": [
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(1)",
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(2)",
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(3)",
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(4)"
    ],
    "stat": [
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(6)",
        ".fgBin.row-button > div[class*='button-green fgButton']:nth-child(7)"
    ],
    "type": [
        "#root-buttons-stats > div:nth-child(1)",
        "#root-buttons-stats > div:nth-child(2)",
        "#root-buttons-stats > div:nth-child(3)"
    ]
}
dropdowns = {
    "time_filter": "#root-menu-time-filter > .fg-dropdown.splits.multi-choice",
    "preset_range": "#root-menu-time-filter > .fg-dropdown.splits.single-choice",
    "groupby": ".fg-dropdown.group-by"
}
splits = {
    "handedness": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(1)",
    "home_away": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(2)",
    "batted_ball": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(3)",
    "situation": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(4)",
    "count": ".fgBin:nth-child(1) > .fg-dropdown.splits.multi-choice:nth-child(5)",
    "batting_order": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(1)",
    "position": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(2)",
    "inning": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(3)",
    "leverage": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(4)",
    "shifts": ".fgBin:nth-child(2) > .fg-dropdown.splits.multi-choice:nth-child(5)",
    "team": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(1)",
    "opponent": ".fgBin:nth-child(3) > .fg-dropdown.splits.multi-choice:nth-child(2)",
}
quick_splits = {
    "batting_home": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(1)",
    "batting_away": ".quick-splits > div:nth-child(1) > div:nth-child(2) > .fgButton:nth-child(2)",
    "vs_lhp": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(1)",
    "vs_lhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(2)",
    "vs_lhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(3)",
    "vs_lhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(4)",
    "vs_lhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(3) > .fgButton:nth-child(5)",
    "vs_rhp": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(1)",
    "vs_rhp_home": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(2)",
    "vs_rhp_away": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(3)",
    "vs_rhp_as_lhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(4)",
    "vs_rhp_as_rhh": ".quick-splits > div:nth-child(1) > div:nth-child(4) > .fgButton:nth-child(5)",
    "pitching_as_sp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(1)",
    "pitching_as_rp": ".quick-splits > div:nth-child(2) > div:nth-child(1) .fgButton:nth-child(2)",
    "pitching_home": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(1)",
    "pitching_away": ".quick-splits > div:nth-child(2) > div:nth-child(2) > .fgButton:nth-child(2)",
    "vs_lhh": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(1)",
    "vs_lhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(2)",
    "vs_lhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(3)",
    "vs_lhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(4)",
    "vs_lhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(3) > .fgButton:nth-child(5)",
    "vs_rhh": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
    "vs_rhh_home": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
    "vs_rhh_away": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
    "vs_rhh_as_rhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)",
    "vs_rhh_as_lhp": ".quick-splits > div:nth-child(2) > div:nth-child(4) > .fgButton:nth-child(1)"
}
switches = {
    "split_teams": "#stack-buttons > div:nth-child(2)",
    "auto_pt": "#stack-buttons > div:nth-child(3)"
}