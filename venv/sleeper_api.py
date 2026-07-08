import requests
import pandas as pd

user_url = "https://api.sleeper.app/v1/user/KyleWurster"
user_data = requests.get(user_url).json()
print(user_data)

user_name = "kylewurster"
user_id = 731000657544359936

league_url = f"https://api.sleeper.app/v1/user/{userid}/leagues/nfl/2026"
league_data = requests.get(league_url).json()
print(league_data)

league_id_freedom = 1182600360190955520

