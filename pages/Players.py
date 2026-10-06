import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import date, time, datetime
from scripts.data_load import (load_master, load_stats)
from sidebar import sidebar

st.set_page_config(layout="centered")
sidebar()
master = load_master()
stats = load_stats()

# create position order
position_order = ["QB", "RB", "WR", "TE"]
# create order as categorical type
# must assign position column as this data type
position_priority = pd.CategoricalDtype(categories=position_order, ordered=True)

primary = "#b5ff00"
secondary = "#404040"

if datetime.now().month >= 1 and datetime.now().month < 9:
    stat_season = stats["season"].max() - 1
else:
    stat_season = stats["season"].max()

stats_current_season = stats[stats["season"] == stat_season]
master_stats_current = master.merge(stats_current_season, on="player_id", how="left")
master_stats_current["position_x"] = master_stats_current["position_x"].astype(position_priority)

games_check = master_stats_current["gp"].isna() | (master_stats_current["gp"] == 0)
null_columns = ["points_freedom", "ppg_freedom", "points_uww", "ppg_uww", "pos_rank_freedom_tot", "rank_freedom_tot", "pos_rank_freedom_per", "rank_freedom_per","pos_rank_uww_tot", "rank_uww_tot", "pos_rank_uww_per", "rank_uww_per"]
master_stats_current.loc[games_check, null_columns] = np.nan

free_agents = master_stats_current.query(f"year_final == {stat_season}")
column_order = ["position_x", "full_name", "team", "age", "years_exp", "apy", "depth_chart_order", "gp","points_freedom", "points_uww","pos_rank_freedom_tot", "pos_rank_uww_tot","rank_freedom_tot", "rank_uww_tot", "ppg_freedom", "ppg_uww", "pos_rank_freedom_per", "pos_rank_uww_per","rank_freedom_per", "rank_uww_per"]
free_agents_df = free_agents[column_order].sort_values(by=["rank_freedom_per"]).dropna(subset=["depth_chart_order"]).rename(columns={"position_x":"Position", "full_name":"Player", "team":"Team", "age":"Age", "years_exp":"Exp", "depth_chart_order":"Depth", "apy":"APY", "gp":"Games", "points_freedom":"Points RRDL", "ppg_freedom":"PPG RRDL", "pos_rank_freedom_tot":"PRank RRDL", "rank_freedom_tot":"Rank RRDL", "pos_rank_freedom_per":"PRank Per RRDL", "rank_freedom_per":"Rank Per RRDL", "points_uww":"Points UWW", "ppg_uww":"PPG UWW", "pos_rank_uww_tot":"PRank UWW", "rank_uww_tot":"Rank UWW", "pos_rank_uww_per":"PRank Per UWW", "rank_uww_per":"Rank Per UWW"})
free_agents_df["APY"] = free_agents_df["APY"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else 0)

select = st.sidebar.selectbox("Choose Analysis:", ["Free Agents", "Breakout Candidates"])

st.header(f"Upcoming Free Agents - {stat_season+1}")
st.dataframe(free_agents_df, hide_index=True)


