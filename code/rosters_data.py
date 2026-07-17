import requests
import pandas as pd

league_id_freedom = "1182600360190955520"
league_id_uww = "1357180013190877184"

def rosters_refresh():
    rosters_data_freedom = requests.get(f"https://api.sleeper.app/v1/league/{league_id_freedom}/rosters").json()
    rosters_data_uww = requests.get(f"https://api.sleeper.app/v1/league/{league_id_uww}/rosters").json()

    rosters_df_raw_freedom = pd.DataFrame(rosters_data_freedom)
    rosters_df_raw_uww = pd.DataFrame(rosters_data_uww)

    # choose owner_id and inner list players to explode list into rows
    rosters_df_filtered_freedom = rosters_df_raw_freedom.filter(items = ["owner_id", "players"]).explode('players')
    rosters_df_freedom = rosters_df_filtered_freedom.rename(columns={"players":"player_id"}).astype({"player_id": str, "owner_id": str})
    rosters_df_filtered_uww = rosters_df_raw_uww.filter(items = ["owner_id", "players"]).explode('players')
    rosters_df_uww = rosters_df_filtered_uww.rename(columns={"players":"player_id"}).astype({"player_id": str, "owner_id": str})

    rosters_df = pd.concat([rosters_df_freedom, rosters_df_uww])
    return rosters_df

