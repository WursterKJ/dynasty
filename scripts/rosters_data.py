import requests
import pandas as pd

league_id_freedom = "1313765911705976832"
league_id_uww = "1357180013190877184"

def rosters_refresh():
    rosters_data_freedom = requests.get(f"https://api.sleeper.app/v1/league/{league_id_freedom}/rosters").json()
    rosters_data_uww = requests.get(f"https://api.sleeper.app/v1/league/{league_id_uww}/rosters").json()

    rosters_df_raw_freedom = pd.DataFrame(rosters_data_freedom)
    rosters_df_raw_uww = pd.DataFrame(rosters_data_uww)

    # choose owner_id and inner list players to explode list into rows
    rosters_df_filtered_freedom = rosters_df_raw_freedom.filter(items = ["owner_id", "players"]).explode('players')
    rosters_df_freedom = rosters_df_filtered_freedom.rename(columns={"players":"player_id", "owner_id":"owner_id_freedom"}).astype({"player_id": str, "owner_id_freedom": str})
    rosters_df_filtered_uww = rosters_df_raw_uww.filter(items = ["owner_id", "players"]).explode('players')
    rosters_df_uww = rosters_df_filtered_uww.rename(columns={"players":"player_id", "owner_id":"owner_id_uww"}).astype({"player_id": str, "owner_id_uww": str})

    rosters_df = rosters_df_freedom.merge(rosters_df_uww, on="player_id", how="outer")
    return rosters_df

