import pandas as pd
import streamlit as st
from code.data_load import (load_master, load_stats)
from dashboard.components.sidebar import sidebar

sidebar()
master = load_master()
stats = load_stats()

users = master["owner_id_uww"].unique()
print(users)

user_select = st.sidebar.selectbox("Choose Manager:", users)

master_df = master.query("owner_id_uww", user_select)

avg_age = master_df.mean("age") 
