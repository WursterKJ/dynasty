from players_data import players_refresh

def data_refresh():
    players = players_refresh()
    master = players.to_csv("data/raw/master.csv", index = False)
    return master