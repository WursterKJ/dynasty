import requests
import pandas as pd

user_url = "https://api.sleeper.app/v1/user/KyleWurster"
user_data = requests.get(user_url).json()
# print(user_data)

user_name = "kylewurster"
user_id = "731000657544359936"

league_url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2026"
league_data = requests.get(league_url).json()
# print(league_data)

league_id_freedom = "1182600360190955520"
league_id_uww = "1357180013190877184"

league_df = pd.DataFrame(league_data)
# print(league_df)

league_url_freedom = f"https://api.sleeper.app/v1/league/{league_id_freedom}"
league_url_uww = f"https://api.sleeper.app/v1/league/{league_id_uww}"
league_data_freedom = requests.get(league_url_freedom).json()
league_data_uww = requests.get(league_url_uww).json()
# league_df_freedom = pd.DataFrame(league_data_freedom)
# league_df_uww = pd.DataFrame(league_data_uww)
print(league_data_freedom)
print(league_data_uww)
