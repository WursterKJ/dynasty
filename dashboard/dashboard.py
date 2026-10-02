import streamlit as st

home = st.Page("pages/Home.py", title="Home", default=True)
rrdl = st.Page("pages/RRDL.py", title="RRDL")
uww = st.Page("pages/UWW.py", title="UWW")
nfl = st.Page("pages/Teams.py", title="NFL")
players = st.Page("pages/Players.py", title="Players")

pages = st.navigation([home, rrdl, uww, nfl, players])
pages.run()