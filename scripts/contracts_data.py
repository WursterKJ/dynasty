import pandas as pd
import nflreadpy as nfl

def contracts_refresh():
    master_data = pd.read_csv("data/master.csv")
    master_list = master_data["search_full_name"].astype(str).to_list()

    search_data = nfl.load_ff_playerids().to_pandas()
    player_search = search_data.filter(items=["merge_name"]).astype(str)
    # must specify column to not chaneg df to series, adjust just inner series of df not full df
    player_search["merge_name"] = player_search["merge_name"].str.replace(" ", "")
    player_search = player_search.query("merge_name in @master_list")

    contracts_data = nfl.load_contracts().to_pandas()
    contracts_data = player_search.join(contracts_data, how="left").query("is_active == True").filter(items=["merge_name", "year_signed", "years", "apy"])

    return contracts_data
