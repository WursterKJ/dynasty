import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, time, datetime
from scripts.data_load import (load_master, load_stats)
from dashboard.sidebar import sidebar

sidebar()
master = load_master()
stats = load_stats()

if datetime.now().month >= 1 and datetime.now().month <= 8:
    stat_season = stats["season"].max() - 1
else:
    stat_season = stats["season"].max()

position_order = ["QB", "RB", "WR", "TE"]
position_priority = pd.CategoricalDtype(categories=position_order, ordered=True)

primary = "#b5ff00"
secondary = "#404040"

# needs fixing but something like this
master_stats = master.merge(stats, on="player_id", how="left")
master_stats_current = master_stats.query("season == @stat_season")

team_df_pos = master_stats.groupby(["team", "position_x"], as_index=False).agg(Season=("season", "first"), Players=("player_id", "count"), Age=("age", "mean"), Exp=("years_exp", "mean"), Thru=("year_final", "mean"), Tot_APY=("apy", "sum"), Avg_APY=("apy", "mean"), Round=("draft_round", "mean"), Overall=("draft_overall", "mean"), Pts_RRDL=("points_freedom", "sum"), PPP_RRDL=("points_freedom", "mean"), PPG_RRDL=("ppg_freedom", "mean"), Starters_RRDL=("starter_freedom", "sum"), Pts_UWW=("points_uww", "sum"), PPP_UWW=("points_uww", "mean"), PPG_UWW=("ppg_uww", "mean"), Starters_UWW=("starter_uww", "sum"))
team_df = master_stats.groupby("team", as_index=False).agg(Season=("season", "first"), Players=("player_id", "count"), Age=("age", "mean"), Exp=("years_exp", "mean"), Thru=("year_final", "mean"), Tot_APY=("apy", "sum"), Avg_APY=("apy", "mean"), Round=("draft_round", "mean"), Overall=("draft_overall", "mean"), Pts_RRDL=("points_freedom", "sum"), PPP_RRDL=("points_freedom", "mean"), PPG_RRDL=("ppg_freedom", "mean"), Starters_RRDL=("starter_freedom", "sum"), Pts_UWW=("points_uww", "sum"), PPP_UWW=("points_uww", "mean"), PPG_UWW=("ppg_uww", "mean"), Starters_UWW=("starter_uww", "sum"))
# rather than explicit rank creation (one script per column) loop through columns, add rank tag, and add to df
rank_columns = ["Age", "Exp", "Thru", "Tot_APY", "Avg_APY", "Round", "Overall", "Pts_RRDL", "PPP_RRDL", "PPG_RRDL", "Starters_RRDL","Pts_UWW", "PPP_UWW", "PPG_UWW", "Starters_UWW"]
team_df[["rank_" + column for column in rank_columns]] = team_df[rank_columns].rank(method="min", ascending=False)

# create team mapping: KC = Kansas City Chiefs as csv file
# download logo page and name as abbreviations = KC.page in logo file for st to pull
# team mapping csv should have tons of team metadata for cool appearance potential (HC, OC, Play Caller, Record, etc.)
teams = pd.read_csv('data/teams.csv')

team_list = teams["team"]
team_select = st.sidebar.selectbox("Choose Team:", team_list)
team_select_df = master_stats_current.query("team == @team_select")

team_roster_df = team_select_df.filter(items=["position_x", "depth_chart_order", "full_name", "age", "years_exp", "draft_round", "draft_overall", "year_final", "apy"]).sort_values(by=["position_x", "depth_chart_order"])
team_stats_df = team_select_df.filter(items=["position_x", "depth_chart_order", "full_name", "points_freedom", "ppg_freedom", "rank_freedom","starters_freedom", "pos_rank_freedom", "points_uww", "ppg_uww", "rank_uww", "pos_rank_uww","starter_uww"]).sort_values(by=["position_x", "depth_chart_order"])

focus_select = st.sidebar.selectbox("Choose Focus:", ["Roster", "Performance"])

st.header(team_select_df["team"])
# st.subheader(teams["play_caller"])
# st.image(f"logo/{{team_select}}.png")

if focus_select == "Roster":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
    with col2:
        st.metric("Exp:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
    with col3:
        st.metric("Round:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
    with col4:
        st.metric("Overall:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
    midcol1, midcol2 = st.columns(2)
    with midcol1:
        st.metric("Thru:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
    with midcol2:
        st.metric("APY:", round(team_roster_df["age"], 1), team_roster_df["rank_age"], "off")
else:
    st.subheader("RRDL")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Points:", round(team_stats_df["points_freedom"], 1), team_stats_df["rank_points_freedom"], "off")
        st.metric("Points:", round(team_stats_df["points_uww"], 1), team_stats_df["rank_points_uww"], "off")
    with col2:
        st.metric("PPP:", round(team_df["points_per_freedom"], 1), team_df["rank_points_per_freedom"], "off")
        st.metric("PPP:", round(team_df["points_per_uww"], 1), team_df["rank_points_per_uww"], "off")
    with col3:
        st.metric("PPG:", round(team_df["ppg_freedom"], 1), team_df["rank_ppg_freedom"], "off")
        st.metric("PPG:", round(team_df["ppg_uww"], 1), team_df["rank_ppg_uww"], "off")
    with col4:
        st.metric("Starters:", team_df["starter_freedom"], team_df["rank_starters_freedom"], "off")
        st.metric("Starters:", team_df["starter_uww"], team_df["rank_starters_uww"], "off")
    st.subheader("UWW")
    st.dataframe(team_stats_df, hide_index=True)
