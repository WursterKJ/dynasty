import requests
import pandas as pd

league_id_freedom = "1182600360190955520"
league_id_uww = "1357180013190877184"

def users_refresh():
    users_data_freedom = requests.get(f"https://api.sleeper.app/v1/league/{league_id_freedom}/users").json()
    users_data_uww = requests.get(f"https://api.sleeper.app/v1/league/{league_id_uww}/users").json()

    users_df_raw_freedom = pd.DataFrame(users_data_freedom)
    users_df_raw_uww = pd.DataFrame(users_data_uww)

    # change user_id columns to match the separated owner_ids from players file, must keep user data as league columns because of duplicate members
    users_df_filtered_freedom = users_df_raw_freedom.filter(items = ["user_id", "display_name"])
    users_df_freedom = users_df_filtered_freedom.rename(columns={"user_id":"owner_id_freedom", "display_name":"display_name_freedom"}).astype({"owner_id_freedom": str})
    users_df_filtered_uww = users_df_raw_uww.filter(items = ["user_id", "display_name"])
    users_df_uww = users_df_filtered_uww.rename(columns={"user_id":"owner_id_uww", "display_name":"display_name_uww"}).astype({"owner_id_uww": str})

    return users_df_freedom, users_df_uww