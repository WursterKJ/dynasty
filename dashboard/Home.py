import streamlit as st
from dashboard.components.sidebar import sidebar

sidebar()
st.title("The Dynasty Dashboard")
st.markdown("""
            Welcome to the Dynasty Dashboard
            """)