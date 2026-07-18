import requests
import pandas as pd
from datetime import datetime, date, time, timedelta


# run only when necessary/periodically
# sleeper does not want to be pulled frequently
# running weekly likely fine (refresh button)

# different years in different URLs, ideally pull 6 years worth of data 
# loop through each year and append files (multiple records per player_id)
# then in dashboard can pull player id and stats by year
current_year = datetime.now().year
first_year = datetime.now().year-6
years = list(range(first_year, current_year+1))
# print(years)

# data has multiple dicts within dicts with player level at highest and stats levels lower
# must convert from player columns to player rows (orient)
# unnest
'''
def stats_refresh():
    for year in years:
'''

stats_url = f"https://api.sleeper.app/v1/stats/nfl/regular/2025"
stats_data = requests.get(stats_url).json()
stats_df_raw = pd.DataFrame.from_dict(stats_data, orient="index").index.name = "player_id"
# stats_df_filtered = stats_df_raw.filter(items=["player_id", "season", "rush_yd"])
print(stats_df_raw)