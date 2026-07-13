import requests
import pandas as pd
import os

# run only when necessary/periodically
# sleeper does not want to be pulled frequently
# may need to run handful of times to update depth chart


# sleeper data is giant nested json with player_id as key and large list of keys within as the pair
# cannot do direct df because of the dict key pairs (dict data type)
# need to un nest the inner key pairs (.json() command creates a dict) into new dict key pairs with column matches
players_url = "https://api.sleeper.app/v1/players/nfl"
players_data = requests.get(players_url).json()
# takes newly converted data (source json to dict and makes data frame from dict)
players_df = pd.DataFrame.from_dict(players_data, orient="index")
print(players_df)
#players_data.to_csv("data/raw/players.csv", index = False)
#print("Successfully Pulled Player Data")

