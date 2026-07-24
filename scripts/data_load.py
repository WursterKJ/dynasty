import pandas as pd
import streamlit as st
from data_refresh import data_refresh

@st.cache_data
def load_master():
    return pd.read_csv("data/master.csv")

@st.cache_data
def load_stats():
    return pd.read_csv("data/master.csv")
