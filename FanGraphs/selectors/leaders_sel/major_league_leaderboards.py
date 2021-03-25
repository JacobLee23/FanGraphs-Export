#! python3
# FanGraphs/selectors/leaders_sel/major_league_leaderboards.py

selections = {
    "group": "#LeaderBoard1_tsGroup",
    "stat": "#LeaderBoard1_tsStats",
    "position": "#LeaderBoard1_tsPosition",
    "type": "#LeaderBoard1_tsType"
}
dropdowns = {
    "league": "#LeaderBoard1_rcbLeague_Input",
    "team": "#LeaderBoard1_rcbTeam_Input",
    "single_season": "#LeaderBoard1_rcbSeason_Input",
    "split": "#LeaderBoard1_rcbMonth_Input",
    "min_pa": "#LeaderBoard1_rcbMin_Input",
    "season1": "#LeaderBoard1_rcbSeason1_Input",
    "season2": "#LeaderBoard1_rcbSeason2_Input",
    "age1": "#LeaderBoard1_rcbAge1_Input",
    "age2": "#LeaderBoard1_rcbAge2_Input"
}
dropdown_options = {
    "league": "#LeaderBoard1_rcbLeague_DropDown",
    "team": "#LeaderBoard1_rcbTeam_DropDown",
    "single_season": "#LeaderBoard1_rcbSeason_DropDown",
    "split": "#LeaderBoard1_rcbMonth_DropDown",
    "min_pa": "#LeaderBoard1_rcbMin_DropDown",
    "season1": "#LeaderBoard1_rcbSeason1_DropDown",
    "season2": "#LeaderBoard1_rcbSeason2_DropDown",
    "age1": "#LeaderBoard1_rcbAge1_DropDown",
    "age2": "#LeaderBoard1_rcbAge2_DropDown"
}
checkboxes = {
    "split_teams": "#LeaderBoard1_cbTeams",
    "active_roster": "#LeaderBoard1_cbActive",
    "hof": "#LeaderBoard1_cbHOF",
    "split_seasons": "#LeaderBoard1_cbSeason",
    "rookies": "#LeaderBoard1_cbRookie"
}
buttons = {
    "season1": "#LeaderBoard1_btnMSeason",
    "season2": "#LeaderBoard1_btnMSeason",
    "age1": "#LeaderBoard1_cmdAge",
    "age2": "#LeaderBoard1_cmdAge"
}
