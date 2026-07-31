import pandas as pd
import streamlit as st
import plotly.express as px
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

users = master["display_name_freedom"].dropna().unique()
users = sorted(users, key=str.lower)

user_select = st.sidebar.selectbox("Choose Manager:", users)
user_select_df = master.query("display_name_freedom == @user_select")

avg_age = round(user_select_df["age"].mean(), 1)
avg_apy = round(user_select_df["apy"].mean(), 2)
avg_depth = round(user_select_df["depth_chart_order"].mean(), 1)
avg_expire = round(user_select_df["year_final"].mean(), 1)

count_pos = user_select_df.value_counts("position").reset_index()
count_pos["position"] = count_pos["position"].astype(position_priority)
count_pos = count_pos.sort_values("position")
count_pos_bar = px.bar(count_pos, x="position", y="count", color_discrete_sequence=[primary])

st.title("The Really Real Dynasty League")
st.subheader(user_select)
st.metric("Age:", avg_age)
st.metric("Depth Chart:", avg_depth)
st.metric("Expiring:", avg_expire)
# format is saying use currency with commas and 2 decimal places after 
st.metric("APY:", f"${avg_apy:,.2f}")
st.plotly_chart(count_pos_bar)
