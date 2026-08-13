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

users = master["display_name_uww"].dropna().unique()
users = sorted(users, key=str.lower)

user_select = st.sidebar.selectbox("Choose Manager:", users)
focus_select = st.sidebar.selectbox("Choose Focus:", ["Roster", "Performance"])

user_select_df = master.query("display_name_uww == @user_select")
user_select_df = user_select_df.merge(stats, how="left", on="player_id").query("season == @stat_season")
user_select_df["position_x"] = user_select_df["position_x"].astype(position_priority)

team_master = master.groupby(["display_name_uww"], as_index=False).agg(age=("age", "mean"), depth=("depth_chart_order", "mean") , expire=("year_final", "mean"), apy=("apy", "mean"))
# individually since different orders (asc/desc)
team_master["rank_age"] = team_master["age"].rank(method="min", ascending=True)
team_master["rank_depth"] = team_master["depth"].rank(method="min", ascending=True)
team_master["rank_expire"] = team_master["expire"].rank(method="min", ascending=False)
team_master["rank_apy"] = team_master["apy"].rank(method="min", ascending=False)
team_master_user = team_master.query("display_name_uww == @user_select")

season_df = master.merge(stats, how="left", on="player_id").query("season == @stat_season")
season_df["position_x"] = season_df["position_x"].astype(position_priority)

team_pivot = season_df.pivot_table(index="display_name_uww", columns="position_x", values="ppg_uww", aggfunc="mean").reset_index()
team_stats = season_df.groupby(["display_name_uww"], as_index=False).agg(tot_pts=("points_uww", "sum"), tot_per_player=("points_uww", "mean"), ppg_player=("ppg_uww", "mean"))
team_stats = team_stats.merge(team_pivot, how="left", on="display_name_uww").rename(columns={"QB":"ppg_qb", "RB":"ppg_rb", "WR":"ppg_wr", "TE":"ppg_te"})
team_stats[["rank_tot_pts", "rank_tot_per_player", "rank_ppg_player", "rank_ppg_qb", "rank_ppg_rb", "rank_ppg_wr", "rank_ppg_te" ]] = team_stats[["tot_pts", "tot_per_player", "ppg_player", "ppg_qb", "ppg_rb", "ppg_wr", "ppg_te"]].rank(method="min", ascending=False)
team_stats_user = team_stats.query("display_name_uww == @user_select")

# take first record of column (always only one row beside headers)
avg_age = round(team_master_user["age"].iloc[0], 1)
avg_apy = round(team_master_user["apy"].iloc[0], 2)
avg_depth = round(team_master_user["depth"].iloc[0], 1)
avg_expire = round(team_master_user["expire"].iloc[0], 1)
rank_avg_age = int(team_master_user["rank_age"].iloc[0])
rank_avg_apy = int(team_master_user["rank_apy"].iloc[0])
rank_avg_depth = int(team_master_user["rank_depth"].iloc[0])
rank_avg_expire = int(team_master_user["rank_expire"].iloc[0])
tot_pts = round(team_stats_user["tot_pts"].iloc[0], 1)
tot_per_player = round(team_stats_user["tot_per_player"].iloc[0], 1)
ppg_player = round(team_stats_user["ppg_player"].iloc[0], 1)
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

count_pos = user_select_df.value_counts("position_x").reset_index().sort_values("position_x")
count_pos_bar = px.bar(count_pos, x="position_x", y="count", color_discrete_sequence=[primary])

master_radar = go.Figure()
# last value repeated to close the shape
master_radar.add_trace(go.Scatterpolar(r=[rank_avg_age, rank_avg_depth, rank_avg_expire, rank_avg_apy, rank_avg_age], theta=["Age", "Depth", "Expiring", "APY", "Age"], fill="toself", fillcolor=primary, mode="lines"))
master_radar.update_layout(polar=dict(
        bgcolor="rgba(0,0,0,0)",        # transparent inside the circle
        radialaxis=dict(
            visible=True,
            range=[10, 1],
            tick0=10,
            dtick=3,
            showticklabels=False,
            linecolor="rgba(0,0,0,0)",
            gridcolor="rgba(128,128,128,0.3)"
        ),
        angularaxis=dict(
            gridcolor="rgba(128,128,128,0.3)",
            linecolor="rgba(0,0,0,0)",  # remove the outer circle border
            showline=False
        )
    )
)

roster_table = user_select_df.sort_values(by=["position_x", "apy"], ascending=[True, False]).filter(items=["position_x", "full_name", "team", "age", "years_exp", "depth_chart_order","year_final", "apy", "draft_year", "draft_round", "draft_overall"]).rename(columns={"position_x":"Position", "full_name":"Player", "team":"Team", "age":"Age", "years_exp":"Year", "depth_chart_order":"Depth", "year_final":"Thru", "apy":"APY", "draft_year":"Draft", "draft_round":"Round", "draft_overall":"Overall"})
# lambda allows assigning variables within set, applies to all values in list/set as x, checks if any APY values null/na, if so return 0
roster_table["APY"] = roster_table["APY"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else 0)
stat_table = user_select_df.sort_values(by=["position_x", "ppg_uww"], ascending=[True, False]).filter(items=["position_x", "full_name", "team", "gp", "points_uww", "pos_rank_uww_tot", "rank_uww_tot", "ppg_uww", "pos_rank_uww_per", "rank_uww_per"]).rename(columns={"position_x":"Position", "full_name":"Player", "team":"Team", "gp":"Games", "points_uww":"Points", "ppg_uww":"PPG", "pos_rank_uww_tot":"PRank", "rank_uww_tot":"Rank", "pos_rank_uww_per":"PRank Per", "rank_uww_per":"Rank Per"})

st.title("The UWW Dynasty League")
if focus_select == "Roster":
    st.header(user_select)
    st.subheader(focus_select)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age:", avg_age, rank_avg_age, "off")
    with col2:
        st.metric("Depth Chart:", avg_depth, rank_avg_depth, "off")
    with col3:
        st.metric("Expiring:", avg_expire, rank_avg_expire, "off")
    # format is saying use currency with commas and 2 decimal places after 
    with col4:
        st.metric("APY:", f"${avg_apy:,.2f}", rank_avg_apy, "off")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(count_pos_bar)       
    with chart_col2:
        st.plotly_chart(master_radar)
    st.dataframe(roster_table, hide_index=True)
else:
    st.header(user_select)
    st.subheader(focus_select)
    topcol1, topcol2, topcol3 = st.columns(3)
    with topcol1:
        st.metric("Points:", tot_pts, rank_tot_pts, "off")
    with topcol2:
        st.metric("PPP:", tot_per_player, rank_tot_per_player, delta_color="off")
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