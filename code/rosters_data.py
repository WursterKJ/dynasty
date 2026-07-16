import requests
import pandas as pd

league_id_freedom = "1182600360190955520"
league_id_uww = "1357180013190877184"

rosters_data_freedom = requests.get(f"https://api.sleeper.app/v1/league/{league_id_freedom}/rosters").json()
rosters_data_uww = requests.get(f"https://api.sleeper.app/v1/league/{league_id_uww}/rosters").json()
