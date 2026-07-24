import requests
import pandas as pd
from datetime import datetime, date, time, timedelta
from players_data import players_refresh, players_list

# run only when necessary/periodically
# sleeper does not want to be pulled frequently
# running weekly likely fine (refresh button)

# different years in different URLs, ideally pull 6 years worth of data 
# loop through each year and append files (multiple records per player_id)
# then in dashboard can pull player id and stats by year

current_year = datetime.now().year
first_year = datetime.now().year-6
years = list(range(first_year, current_year+1))

# import players_df from players refresh
players_df = players_refresh()
players_ids = players_list(players_df)

# initialize empty array for appended stats yearly data later on
stats_df_all = []

def stats_refresh():
    for year in years:
        stats_url = f"https://api.sleeper.app/v1/stats/nfl/regular/{year}"
        stats_data = requests.get(stats_url).json()
        stats_df_raw = pd.DataFrame.from_dict(stats_data, orient="index")
        stats_df_raw.index.name = "player_id"
        stats_df_raw = stats_df_raw.reset_index()
        stats_df_filtered = stats_df_raw.filter(items=["player_id", "gp", "pass_att", "pass_cmp", "pass_yd", "pass_td", "pass_int", "pass_sack", "pass_air_yd", "pass_rz_att", "rush_att", "rush_yd", "rush_td", "rush_btkl", "rush_yac", "rush_rz_att", "rush_tkl_loss", "rec", "rec_tgt", "rec_yd", "rec_td", "rec_air_yd", "rec_yar", "rec_drop", "rec_rz_tgt", "fum", "fum_lost", "st_td", "off_snp", "tm_off_snp", "bonus_pass_yd_300", "bonus_pass_yd_400", "bonus_rush_yd_100", "bonus_rush_yd_200", "bonus_rec_yd_100", "bonus_rec_yd_200"])
        stats_df_filtered = stats_df_filtered.astype({"player_id": str})
        stats_df_filtered["season"] = year
        # take only player ids of new df where id exists in players_list from other player data pull
        stats_df = stats_df_filtered[stats_df_filtered["player_id"].isin(players_ids)]
        # append all 6 dataframes in list (append is list function)
        stats_df_all.append(stats_df)
    stats_df = pd.concat(stats_df_all, ignore_index=True)
    return stats_df
