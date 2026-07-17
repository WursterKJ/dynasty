from players_data import players_refresh
from trending_data import trending_refresh
from rosters_data import rosters_refresh
from users_data import users_refresh

def data_refresh():
    players = players_refresh()
    trending = trending_refresh()
    rosters = rosters_refresh()
    users_freedom, users_uww = users_refresh()


    players_trending = players.merge(trending, on="player_id", how="left")
    players_rosters = players_trending.merge(rosters, on="player_id", how="left")
    players_rosters_freedom = players_rosters.merge(users_freedom, on=["owner_id_freedom"], how="left")
    master = players_rosters_freedom.merge(users_uww, on=["owner_id_uww"], how="left")

    master.to_csv("data/raw/master.csv", index = False)
    return master

data_refresh()
print("Successfully created data files")