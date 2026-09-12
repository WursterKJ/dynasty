import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, time, datetime
from scripts.data_load import (load_master, load_stats)
from dashboard.sidebar import sidebar

st.set_page_config(layout="centered")
sidebar()
master = load_master()
stats = load_stats()

if datetime.now().month >= 1 and datetime.now().month <= 9:
    stat_season = stats["season"].max() - 1
else:
    stat_season = stats["season"].max()

position_order = ["QB", "RB", "WR", "TE"]
position_priority = pd.CategoricalDtype(categories=position_order, ordered=True)

primary = "#b5ff00"
secondary = "#404040"

master_stats = master.merge(stats, on="player_id", how="left")
master_stats_current = master_stats.query("season == @stat_season")

team_df_pos = master_stats_current.groupby(["team", "position_x"], as_index=False).agg(Season=("season", "first"), Players=("player_id", "count"), Age=("age", "mean"), Exp=("years_exp", "mean"), Thru=("year_final", "mean"), Tot_APY=("apy", "sum"), Avg_APY=("apy", "mean"), Round=("draft_round", "mean"), Overall=("draft_overall", "mean"), Pts_RRDL=("points_freedom", "sum"), PPP_RRDL=("points_freedom", "mean"), PPG_RRDL=("ppg_freedom", "mean"), Starters_RRDL=("starter_freedom", "sum"), Pts_UWW=("points_uww", "sum"), PPP_UWW=("points_uww", "mean"), PPG_UWW=("ppg_uww", "mean"), Starters_UWW=("starter_uww", "sum"))
team_df = master_stats_current.groupby("team", as_index=False).agg(Season=("season", "first"), Players=("player_id", "count"), Age=("age", "mean"), Exp=("years_exp", "mean"), Thru=("year_final", "mean"), Tot_APY=("apy", "sum"), Avg_APY=("apy", "mean"), Round=("draft_round", "mean"), Overall=("draft_overall", "mean"), Pts_RRDL=("points_freedom", "sum"), PPP_RRDL=("points_freedom", "mean"), PPG_RRDL=("ppg_freedom", "mean"), Starters_RRDL=("starter_freedom", "sum"), Pts_UWW=("points_uww", "sum"), PPP_UWW=("points_uww", "mean"), PPG_UWW=("ppg_uww", "mean"), Starters_UWW=("starter_uww", "sum"))
# rather than explicit rank creation (one script per column) loop through columns, add rank tag, and add to df
rank_columns_desc = ["Exp", "Thru", "Tot_APY", "Avg_APY", "Pts_RRDL", "PPP_RRDL", "PPG_RRDL", "Starters_RRDL","Pts_UWW", "PPP_UWW", "PPG_UWW", "Starters_UWW"]
rank_columns_asc = ["Age", "Round", "Overall"]
team_df[["rank_" + column for column in rank_columns_desc]] = team_df[rank_columns_desc].rank(method="min", ascending=False).astype(int)
team_df[["rank_" + column for column in rank_columns_asc]] = team_df[rank_columns_asc].rank(method="min", ascending=True).astype(int)
rank_values = ["rank_Age", "rank_Exp", "rank_Round", "rank_Overall", "rank_Thru", "rank_Tot_APY", "rank_Avg_APY", "rank_Pts_RRDL", "rank_PPP_RRDL", "rank_PPG_RRDL", "rank_Starters_RRDL","rank_Pts_UWW", "rank_PPP_UWW", "rank_PPG_UWW", "rank_Starters_UWW"]
team_df[["color_" + column for column in rank_values]] = team_df[rank_values].map(lambda value: "blue" if value <= 8 else "green" if value <= 16 else "orange" if value <=24 else "red")

select = st.sidebar.selectbox("Choose Analysis:", ["Free Agents", "Breakout Candidates"])

st.header(f"Upcoming Free Agents - {stat_season}")

