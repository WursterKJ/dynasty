import streamlit as st
from sidebar import sidebar

sidebar()
st.title("The Dynasty Dashboard")
st.markdown("""
            Welcome to the Dynasty Dashboard

            With sleeper.com's fantasy league data being free for public use through the Sleeper API, 
            this dashboard was made to find deeper insights of the best two dynasty leagues of the 21st century.
            In addition, this has been a rewarding project to improve and learn Python through pandas and streamlit.

            The best visual expereince will be provided through the dark theme (top right corner > three dots > dark).
            Metrics are calculated to compare league rosters' performance and player makeup. If you come across any
            issues, bugs, or miscalculations, please email me at kylewurster28@gmail.com. Enjoy :)

            Glossary:

            Roster:
            Age: Average/age of all active players
            Experience: Average/years of NFL experience (rookies zero)
            Depth Chart: Average/depth chart position, representing a player's order on their NFL team
            Thru: Average/the last NFL season the player's current contract (2026 = free agent following 2026 season)
            APY: Average annual value for the player's current contract
            Total APY: Sum total of all players' APY's
            Average APY: Average of all players' APY's
            Draft: Year the player was drafted
            Round: Average draft round of all active players
            Overall: Average overall draft position of all active players

            Performance:
            Points: Total fantasy points scored for the current or previous season
            PPP: Average points per player on the roster who played in at least one game
            PPG: Average points per game per player on the roster who played in at least one game
            Starters: Number of players who ranked high enough by position to be a fantasy starter
            Rank: Overall fantasy rank, all positions
            PRank: Positional fantasy rank
            Per: Ranks on per game basis rather than total points scored
            **All scoring metrics calculated using league specific scoring settings
            """)


