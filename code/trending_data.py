import requests
import pandas as pd

# since trending data much smaller, not nested dicts, instead list key pairs
# do not need from_dict can go straight through df

trending_up_url = "https://api.sleeper.app/v1/players/nfl/trending/add?lookback_hours=48&limit=100"
trending_down_url = "https://api.sleeper.app/v1/players/nfl/trending/drop?lookback_hours=48&limit=100"

def trending_refresh():
    trending_up_data = requests.get(trending_up_url).json()
    trending_down_data = requests.get(trending_down_url).json()
    # rename columns once df by rename columns and create new key pairs
    trending_up_df = pd.DataFrame(trending_up_data).rename(columns={"count" : "adds"})
    trending_down_df = pd.DataFrame(trending_down_data).rename(columns={"count" : "drops"})
    trending_df = trending_up_df.join(trending_down_df, on="player_id", how="outer")
    trending_df.to_csv("data/raw/trending.csv", index = False)
    return trending_df

# trending_up_df.to_csv("data/raw/trending_up.csv", index = False)
# trending_down_df.to_csv("data/raw/trending_down.csv", index = False)
#trending_df.to_csv("data/raw/trending.csv", index = False)
trending_refresh()
print("Successfully Pulled Player Data")