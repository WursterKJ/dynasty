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

season_df = master.merge(stats, how="left", on="player_id").query("season == @stat_season")
season_df["position"] = season_df["position"].astype(position_priority)

team_pivot = season_df.pivot_table(index="display_name_freedom", columns="position", values="ppg_freedom", aggfunc="mean").reset_index()
team_stats = season_df.groupby(["display_name_freedom"], as_index=False).agg(tot_pts=("points_freedom", "sum"), tot_per_player=("points_freedom", "mean"), ppg_player=("ppg_freedom", "mean"))
team_stats = team_stats.merge(team_pivot, how="left", on="display_name_freedom").rename(columns={"QB":"ppg_qb", "RB":"ppg_rb", "WR":"ppg_wr", "TE":"ppg_te"})
team_stats[["rank_tot_pts", "rank_tot_per_player", "rank_ppg_player", "rank_ppg_qb", "rank_ppg_rb", "rank_ppg_wr", "rank_ppg_te" ]] = team_stats[["tot_pts", "tot_per_player", "ppg_player", "ppg_qb", "ppg_rb", "ppg_wr", "ppg_te"]].rank(method="min", ascending=False)
team_stats_user = team_stats.query("display_name_freedom == @user_select")

avg_age = round(user_select_df["age"].mean(), 1)
avg_apy = round(user_select_df["apy"].mean(), 2)
avg_depth = round(user_select_df["depth_chart_order"].mean(), 1)
avg_expire = round(user_select_df["year_final"].mean(), 1)

# take first record of column (always only one row beside headers)
tot_pts = round(team_stats_user["tot_pts"].iloc[0], 1)
tot_per_player = round(team_stats_user["tot_per_player"].iloc[0], 1)
ppg_player = tot_pts = round(team_stats_user["ppg_player"].iloc[0], 1)
ppg_qb = round(team_stats_user["ppg_qb"].iloc[0], 1)
ppg_rb = round(team_stats_user["ppg_rb"].iloc[0], 1)
ppg_wr = round(team_stats_user["ppg_wr"].iloc[0], 1)
ppg_te = round(team_stats_user["ppg_te"].iloc[0], 1)
rank_tot_pts = int(team_stats_user["rank_tot_pts"].iloc[0])
rank_tot_per_player = int(team_stats_user["rank_tot_per_player"].iloc[0])
rank_ppg_player = int(team_stats_user["rank_ppg_player"].iloc[0])
rank_ppg_qb = int(team_stats_user["rank_ppg_qb"].iloc[0])
rank_ppg_rb = int(team_stats_user["rank_ppg_rb"].iloc[0])
rank_ppg_wr = int(team_stats_user["rank_ppg_wr"].iloc[0])
rank_ppg_te = int(team_stats_user["rank_ppg_te"].iloc[0])

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
    topcol1, topcol2, topcol3 = st.columns(3)
    with topcol1:
        st.metric("Points:", tot_pts, rank_tot_pts, "off")
    with topcol2:
        st.metric("Points per:", tot_per_player, rank_tot_per_player, "off")
    with topcol3:
        st.metric("PPG:", ppg_player, rank_ppg_player, "off")
    midcol1, midcol2, midcol3, midcol4 = st.columns(4)
    with midcol1:
        st.metric("QB:", ppg_qb, rank_ppg_qb, "off")
    with midcol2:    
        st.metric("RB:", ppg_rb, rank_ppg_rb, "off")
    with midcol3:
        st.metric("WR:", ppg_wr, rank_ppg_wr, "off")
    with midcol4:
        st.metric("TE:", ppg_te, rank_ppg_te, "off")
    st.dataframe(stat_table, hide_index=True, use_container_width=True)
