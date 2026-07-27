import pandas as pd
import nflreadpy as nfl
import re
from datetime import datetime, date, time

# need to manually make merge_name in contract file since no common ids. this is straight from claude/nfldataverse github code
# review and learn what this regex is doing for future reference

def contracts_refresh():
    master_data = pd.read_csv("data/master.csv")
    master_list = master_data["search_full_name"].astype(str).to_list()

    search_data = nfl.load_ff_playerids().to_pandas()
    player_search = search_data.filter(items=["merge_name", "sleeper_id"]).astype(str)
    # must specify column to not change df to series, adjust just inner series of df not full df
    player_search["merge_name"] = player_search["merge_name"].str.replace(" ", "")
    player_search = player_search.query("merge_name in @master_list")

    contracts_data = nfl.load_contracts().to_pandas()

    def clean_name(name):
        name = str(name).lower()
        name = re.sub(r"[.\'\-]", "", name)              # strip punctuation
        name = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", name)  # strip suffixes
        name = re.sub(r"\s+", " ", name).strip()          # collapse whitespace
        name = name.replace(" ", "")                       # your inner-space removal
        return name
    # creates merge_name column which is taking player name column and running through the clean name function
    # merge into master list including sleeper id which allows two join options (find which most accurate)
    contracts_data["merge_name"] = contracts_data["player"].apply(clean_name)
    contracts_data = player_search.merge(contracts_data, on="merge_name", how="left").query("is_active == True").filter(items=["merge_name", "sleeper_id", "year_signed", "years", "apy", "draft_year", "draft_round", "draft_overall"])
    contracts_data["year_final"] = contracts_data["year_signed"].astype("Int64") + contracts_data["years"] - 1
    contracts_data["years_remaining"] = contracts_data["year_final"] - datetime.now().year

    return contracts_data
