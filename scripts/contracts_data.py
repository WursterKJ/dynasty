import pandas as pd
import nflreadpy as nfl

def contracts_refresh():
    master_data = pd.read_csv("data/master.csv")
    master_list = master_data["player_id"].astype(str).to_list()

    ids_data = nfl.load_ff_playerids().to_pandas()
    sleeper_ids = ids_data.filter(items=["sleeper_id"]).astype("Int64")
    sleeper_ids = sleeper_ids.astype(str).query("sleeper_id in @master_list")

    contracts_data = nfl.load_contracts().to_pandas()
    contracts_data = sleeper_ids.join(contracts_data, how="left").query("is_active == True").filter(items=["sleeper_id", "year_signed", "years", "apy"])

    return contracts_data

