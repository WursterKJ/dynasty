import requests
import pandas as pd

# run only when necessary/periodically
# sleeper does not want to be pulled frequently
# may need to run handful of times to update depth chart

# sleeper data is giant nested json with player_id as key and large list of keys within as the pair
# cannot do direct df because of the dict key pairs (dict data type)
# need to un nest the inner key pairs (.json() command creates a dict) into new dict key pairs with column matches

players_url = "https://api.sleeper.app/v1/players/nfl"

def players_refresh():
    players_data = requests.get(players_url).json()
    # takes newly converted data (source json to dict and makes data frame from dict)
    players_df_raw = pd.DataFrame.from_dict(players_data, orient="index")
    # orient index flips columns and rows using indices as columns
    players_filtered = players_df_raw.query("active == True and status == 'Active' and (position == 'QB' or position == 'RB' or position == 'WR' or position == 'TE')")
    players_filtered_columns = players_filtered.filter(items = ["player_id", "full_name", "position", "team", "number", "college", "years_exp", "birth_date", "age", "height", "weight", "depth_chart_order", "injury_status", "injury_body_part", "stats_id", "search_full_name"])
    players_df = players_filtered_columns.astype({"player_id": str})
        # print(players_filtered)
        # players_filtered_columns.to_csv("data/raw/players.csv", index = False)
    return players_df


