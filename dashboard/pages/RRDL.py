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
user_select_df["position_x"] = user_select_df["position_x"].astype(position_priority)

team_master = master.groupby(["display_name_freedom"], as_index=False).agg(age=("age", "mean"), depth=("depth_chart_order", "mean") , expire=("year_final", "mean"), apy=("apy", "mean"), tot_apy=("apy", "sum"), exp=("years_exp", "mean"))
# individually since different orders (asc/desc)
team_master["rank_age"] = team_master["age"].rank(method="min", ascending=True)
team_master["rank_depth"] = team_master["depth"].rank(method="min", ascending=True)
team_master["rank_expire"] = team_master["expire"].rank(method="min", ascending=False)
team_master["rank_apy"] = team_master["apy"].rank(method="min", ascending=False)
team_master["rank_tot_apy"] = team_master["tot_apy"].rank(method="min", ascending=False)
team_master["rank_exp"] = team_master["exp"].rank(method="min", ascending=False)
team_master_user = team_master.query("display_name_freedom == @user_select")

season_df = master.merge(stats, how="left", on="player_id").query("season == @stat_season")
season_df["position_x"] = season_df["position_x"].astype(position_priority)

team_pivot = season_df.pivot_table(index="display_name_freedom", columns="position_x", values="ppg_freedom", aggfunc="mean").reset_index()
team_stats = season_df.groupby(["display_name_freedom"], as_index=False).agg(tot_pts=("points_freedom", "sum"), tot_per_player=("points_freedom", "mean"), ppg_player=("ppg_freedom", "mean"), starter_freedom=("starter_freedom", "sum"))
team_stats = team_stats.merge(team_pivot, how="left", on="display_name_freedom").rename(columns={"QB":"ppg_qb", "RB":"ppg_rb", "WR":"ppg_wr", "TE":"ppg_te"})
team_stats[["rank_tot_pts", "rank_tot_per_player", "rank_ppg_player", "rank_ppg_qb", "rank_ppg_rb", "rank_ppg_wr", "rank_ppg_te", "rank_starters"]] = team_stats[["tot_pts", "tot_per_player", "ppg_player", "ppg_qb", "ppg_rb", "ppg_wr", "ppg_te", "starter_freedom"]].rank(method="min", ascending=False)
team_stats_user = team_stats.query("display_name_freedom == @user_select")

# take first record of column (always only one row beside headers)
avg_age = round(team_master_user["age"].iloc[0], 1)
avg_apy = round(team_master_user["apy"].iloc[0], 1)
avg_depth = round(team_master_user["depth"].iloc[0], 1)
avg_expire = round(team_master_user["expire"].iloc[0], 1)
avg_exp = round(team_master_user["exp"].iloc[0], 1)
tot_apy = round(team_master_user["tot_apy"].iloc[0], 1)
rank_avg_age = int(team_master_user["rank_age"].iloc[0])
rank_avg_apy = int(team_master_user["rank_apy"].iloc[0])
rank_tot_apy = int(team_master_user["rank_tot_apy"].iloc[0])
rank_avg_exp = int(team_master_user["rank_exp"].iloc[0])
rank_avg_depth = int(team_master_user["rank_depth"].iloc[0])
rank_avg_expire = int(team_master_user["rank_expire"].iloc[0])
tot_pts = int(team_stats_user["tot_pts"].iloc[0])
tot_per_player = int(team_stats_user["tot_per_player"].iloc[0])
ppg_player = round(team_stats_user["ppg_player"].iloc[0], 1)
ppg_qb = round(team_stats_user["ppg_qb"].iloc[0], 1)
ppg_rb = round(team_stats_user["ppg_rb"].iloc[0], 1)
ppg_wr = round(team_stats_user["ppg_wr"].iloc[0], 1)
ppg_te = round(team_stats_user["ppg_te"].iloc[0], 1)
starters = int(team_stats_user["starter_freedom"].iloc[0])
rank_tot_pts = int(team_stats_user["rank_tot_pts"].iloc[0])
rank_tot_per_player = int(team_stats_user["rank_tot_per_player"].iloc[0])
rank_ppg_player = int(team_stats_user["rank_ppg_player"].iloc[0])
rank_ppg_qb = int(team_stats_user["rank_ppg_qb"].iloc[0])
rank_ppg_rb = int(team_stats_user["rank_ppg_rb"].iloc[0])
rank_ppg_wr = int(team_stats_user["rank_ppg_wr"].iloc[0])
rank_ppg_te = int(team_stats_user["rank_ppg_te"].iloc[0])
rank_starters = int(team_stats_user["rank_starters"].iloc[0])

rank_master_values = ["rank_age", "rank_apy", "rank_tot_apy", "rank_expire", "rank_exp", "rank_depth"]
rank_stat_values = ["rank_tot_pts", "rank_tot_per_player", "rank_ppg_player", "rank_ppg_qb", "rank_ppg_rb", "rank_ppg_wr", "rank_ppg_te", "rank_starters"]
team_master_user[["color_" + column for column in rank_master_values]] = team_master_user[rank_master_values].map(lambda value: "blue" if value <= 2 else "green" if value <= 5 else "orange" if value <=8 else "red")
team_stats_user[["color_" + column for column in rank_stat_values]] = team_stats_user[rank_stat_values].map(lambda value: "blue" if value <= 2 else "green" if value <= 5 else "orange" if value <=8 else "red")

count_pos = user_select_df.value_counts("position_x").reset_index().sort_values("position_x")
count_pos_bar = px.bar(count_pos, x="position_x", y="count", color_discrete_sequence=[primary])

master_radar = go.Figure()
# last value repeated to close the shape
master_radar.add_trace(go.Scatterpolar(r=[rank_avg_age, rank_avg_depth, rank_avg_expire, rank_avg_apy, rank_avg_age], theta=["Age", "Depth", "Expiring", "APY", "Age"], fill="toself", fillcolor=primary, mode="lines"))
# polar is all about chart background format, bgcolor is transparent background, 
master_radar.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]),
        radialaxis=dict(visible=True, range=[10, 1], tick0=10, dtick=3, showticklabels=False, ticks="", linecolor="rgba(0,0,0,0)", gridcolor="rgba(128,128,128,0.3)"),
        angularaxis=dict(gridcolor="rgba(128,128,128,0.3)",linecolor="rgba(128,128,128,0.3)", showgrid=False, rotation=90)))

roster_table = user_select_df.sort_values(by=["position_x", "apy"], ascending=[True, False]).filter(items=["position_x", "full_name", "team", "age", "years_exp", "depth_chart_order","year_final", "apy", "draft_year", "draft_round", "draft_overall"]).rename(columns={"position_x":"Position", "full_name":"Player", "team":"Team", "age":"Age", "years_exp":"Exp", "depth_chart_order":"Depth", "year_final":"Thru", "apy":"APY", "draft_year":"Draft", "draft_round":"Round", "draft_overall":"Overall"})
# lambda allows assigning variables within set, applies to all values in list/set as x, checks if any APY values null/na, if so return 0
roster_table["APY"] = roster_table["APY"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else 0)
stat_table = user_select_df.sort_values(by=["position_x", "ppg_freedom"], ascending=[True, False]).filter(items=["position_x", "full_name", "team", "gp", "points_freedom", "pos_rank_freedom_tot", "rank_freedom_tot", "ppg_freedom", "pos_rank_freedom_per", "rank_freedom_per"]).rename(columns={"position_x":"Position", "full_name":"Player", "team":"Team", "gp":"Games", "points_freedom":"Points", "ppg_freedom":"PPG", "pos_rank_freedom_tot":"PRank", "rank_freedom_tot":"Rank", "pos_rank_freedom_per":"PRank Per", "rank_freedom_per":"Rank Per"})

st.title("The Really Real Dynasty League")
if focus_select == "Roster":
    st.header(user_select)
    st.subheader(focus_select)
    col1, rcol1, col2, rcol2, col3, rcol3 = st.columns(6, vertical_alignment="center", gap="xxsmall")
    with col1:
        st.metric("Age:", avg_age)
    with rcol1:
        st.badge(str(rank_avg_age), color=team_master_user["color_rank_age"].iloc[0])
    with col2:
        st.metric("Experience:", avg_exp)
    with rcol2:
        st.badge(str(rank_avg_exp), color=team_master_user["color_rank_exp"].iloc[0])
    with col3:
        st.metric("Depth Chart:", avg_depth)
    with rcol3:
        st.badge(str(rank_avg_depth), color=team_master_user["color_rank_depth"].iloc[0])
    col1, rcol1, col2, rcol2, col3, rcol3 = st.columns(6, vertical_alignment="center", gap="xxsmall")
    with col1:
        st.metric("Thru:", avg_expire)
    with rcol1:
        st.badge(str(rank_avg_expire), color=team_master_user["color_rank_expire"].iloc[0])
    with col2:
        # format is saying use currency with commas and 2 decimal places after 
        st.metric("Total APY:", f"${tot_apy:,.1f}")
    with rcol2:
        st.badge(str(rank_tot_apy), color=team_master_user["color_rank_tot_apy"].iloc[0])
    with col3:
        st.metric("Average APY:", f"${avg_apy:,.1f}")
    with rcol3:
        st.badge(str(rank_avg_apy), color=team_master_user["color_rank_apy"].iloc[0])
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(count_pos_bar)       
    with chart_col2:
        st.plotly_chart(master_radar)
    st.dataframe(roster_table, hide_index=True)
else:
    st.header(user_select)
    st.subheader(focus_select)
    col1, rcol1, col2, rcol2, col3, rcol3, col4, rcol4 = st.columns(8, vertical_alignment="center", gap="xxsmall")
    with col1:
        st.metric("Points:", tot_pts)
    with rcol1:
        st.badge(str(rank_tot_pts), color=team_stats_user["color_rank_tot_pts"].iloc[0])
    with col2:
        st.metric("PPP:", tot_per_player)
    with rcol2:
        st.badge(str(rank_tot_per_player), color=team_stats_user["color_rank_tot_per_player"].iloc[0])
    with col3:
        st.metric("PPG:", ppg_player)
    with rcol3:
        st.badge(str(rank_ppg_player), color=team_stats_user["color_rank_ppg_player"].iloc[0])
    with col4:
        st.metric("Starters:", starters)
    with rcol4:
        st.badge(str(rank_starters), color=team_stats_user["color_rank_starters"].iloc[0])
    midcol1, midrcol1, midcol2, midrcol2, midcol3, midrcol3, midcol4, midrcol4 = st.columns(8, vertical_alignment="center", gap="xxsmall")
    with midcol1:
        st.metric("QB:", ppg_qb)
    with midrcol1:
        st.badge(str(rank_ppg_qb), color=team_stats_user["color_rank_ppg_qb"].iloc[0])
    with midcol2:
        st.metric("RB:", ppg_rb)
    with midrcol2:
        st.badge(str(rank_ppg_rb), color=team_stats_user["color_rank_ppg_rb"].iloc[0])
    with midcol3:
        st.metric("WR:", ppg_wr)
    with midrcol3:
        st.badge(str(rank_ppg_wr), color=team_stats_user["color_rank_ppg_wr"].iloc[0])
    with midcol4:
        st.metric("TE:", ppg_te)
    with midrcol4:
        st.badge(str(rank_ppg_te), color=team_stats_user["color_rank_ppg_te"].iloc[0])
    st.dataframe(stat_table, hide_index=True, use_container_width=True)
