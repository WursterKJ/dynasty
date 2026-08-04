import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import date, time, datetime
from scripts.data_load import (load_master, load_stats)
from dashboard.sidebar import sidebar

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

if datetime.now().month >= 1 and datetime.now().month <= 8:
    stat_season = stats["season"].max() - 1
else:
    stat_season = stats["season"].max()

users = master["display_name_freedom"].dropna().unique()
users = sorted(users, key=str.lower)

user_select = st.sidebar.selectbox("Choose Manager:", users)
focus_select = st.sidebar.selectbox("Choose Focus:", ["Roster", "Performance"])

user_select_df = master.query("display_name_freedom == @user_select")
user_select_df = user_select_df.merge(stats, how="left", on="player_id").query("season == @stat_season")
user_select_df["position"] = user_select_df["position"].astype(position_priority)

user_select_qb = user_select_df.query("position == 'QB'")
user_select_rb = user_select_df.query("position == 'RB'")
user_select_wr = user_select_df.query("position == 'WR'")
user_select_te = user_select_df.query("position == 'TE'")

avg_age = round(user_select_df["age"].mean(), 1)
avg_apy = round(user_select_df["apy"].mean(), 2)
avg_depth = round(user_select_df["depth_chart_order"].mean(), 1)
avg_expire = round(user_select_df["year_final"].mean(), 1)

tot_pts_max = round(user_select_df["points_freedom"].sum(), 1)
avg_pts_max = round((user_select_df["points_freedom"].sum())/17, 1)

avg_ppg = round(user_select_df["ppg_freedom"].mean(), 1)
avg_ppg_qb = round(user_select_qb["ppg_freedom"].mean(), 1)
avg_ppg_rb = round(user_select_rb["ppg_freedom"].mean(), 1)
avg_ppg_wr = round(user_select_wr["ppg_freedom"].mean(), 1)
avg_ppg_te = round(user_select_te["ppg_freedom"].mean(), 1)

count_pos = user_select_df.value_counts("position").reset_index().sort_values("position")
count_pos_bar = px.bar(count_pos, x="position", y="count", color_discrete_sequence=[primary])

roster_table = user_select_df.sort_values("position").filter(items=["position", "full_name", "team", "age", "years_exp", "depth_chart_order","year_final", "apy", "draft_year", "draft_round", "draft_overall"]).rename(columns={"position":"Position", "full_name":"Player", "team":"Team", "age":"Age", "years_exp":"Year", "depth_chart_order":"Depth", "year_final":"Thru", "apy":"APY", "draft_year":"Draft", "draft_round":"Round", "draft_overall":"Overall"})
# lambda allows assigning variables within set, applies to all values in list/set as x, checks if any APY values null/na, if so return 0
roster_table["APY"] = roster_table["APY"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else 0)
stat_table = user_select_df.sort_values("position").filter(items=["position", "full_name", "team", "gp", "points_freedom", "ppg_freedom"]).rename(columns={"position":"Position", "full_name":"Player", "team":"Team", "gp":"Games", "points_freedom":"Points", "ppg_freedom":"PPG"})

st.title("The Really Real Dynasty League")
if focus_select == "Roster":
    st.header(user_select)
    st.subheader(focus_select)
    st.metric("Age:", avg_age)
    st.metric("Depth Chart:", avg_depth)
    st.metric("Expiring:", avg_expire)
    # format is saying use currency with commas and 2 decimal places after 
    st.metric("APY:", f"${avg_apy:,.2f}")
    st.plotly_chart(count_pos_bar)
    st.dataframe(roster_table, hide_index=True)
else:
    st.header(user_select)
    st.subheader(focus_select)
    st.metric("Points:", tot_pts_max)
    st.metric("Points per:", avg_pts_max)
    st.metric("PPG:", avg_ppg)
    st.metric("QB:", avg_ppg_qb)
    st.metric("RB:", avg_ppg_rb)
    st.metric("WR:", avg_ppg_wr)
    st.metric("TE:", avg_ppg_te)
    st.dataframe(stat_table, hide_index=True)
