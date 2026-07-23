import streamlit as st
from data_refresh import data_refresh

def sidebar():
    st.sidebar.title("Dynasty Dashboard")
    if st.sidebar.button("Refresh Data"):
        with st.spinner("Refreshing..."):
            data_refresh()
            st.cache_data.clear()
        st.success("Refresh Complete")
        st.rerun
    return sidebar()

        