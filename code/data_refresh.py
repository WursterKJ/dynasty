from players_data import players_refresh
from trending_data import trending_refresh
from rosters_data import rosters_refresh

def data_refresh():
    players = players_refresh()
    trending = trending_refresh()
    rosters = rosters_refresh()

    players_trending = players.merge(trending, on="player_id", how="left")
    master = players_trending.merge(rosters, on="player_id", how="left")

    master.to_csv("data/raw/master.csv", index = False)
    return master