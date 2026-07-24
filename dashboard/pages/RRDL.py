import pandas as pd
import streamlit as st
from scripts.data_load import (load_master, load_stats)
from dashboard.sidebar import sidebar

sidebar()
master = load_master()
stats = load_stats()

users = master["display_name_freedom"].dropna().unique()
users = sorted(users, key=str.lower)

user_select = st.sidebar.selectbox("Choose Manager:", users)
user_select_df = master.query("display_name_freedom == @user_select")

avg_age = round(user_select_df["age"].mean(), 1)

st.title("The Really Real Dynasty League")
st.metric("Age:", avg_age)