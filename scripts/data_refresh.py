from scripts.players_data import players_refresh
from scripts.trending_data import trending_refresh
from scripts.rosters_data import rosters_refresh
from scripts.users_data import users_refresh
from scripts.stats_data import stats_refresh
from scripts.contracts_data import contracts_refresh

def data_refresh():
    players = players_refresh()
    trending = trending_refresh()
    rosters = rosters_refresh()
    users_freedom, users_uww = users_refresh()
    stats = stats_refresh()
    contracts = contracts_refresh()

    players_trending = players.merge(trending, on="player_id", how="left")
    players_rosters = players_trending.merge(rosters, on="player_id", how="left")
    players_rosters_freedom = players_rosters.merge(users_freedom, on="owner_id_freedom", how="left")
    players_rosters_all = players_rosters_freedom.merge(users_uww, on="owner_id_uww", how="left")
    master = players_rosters_all.merge(contracts, left_on="player_id", right_on="sleeper_id", how="left")
    master = master.drop_duplicates()

    stats.to_csv("data/stats.csv", index = False)
    master.to_csv("data/master.csv", index = False)
    return master, stats

# comment this code out when ready to deploy dashboard
# data_refresh()
# print("Successfully created data files")

