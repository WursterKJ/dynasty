import pandas as pd
import requests

league_id_freedom = "1182600360190955520"
league_id_uww = "1357180013190877184"

def scoring_refresh():
    scoring_data_freedom = requests.get(f"https://api.sleeper.app/v1/league/{league_id_freedom}").json()
    scoring_data_uww = requests.get(f"https://api.sleeper.app/v1/league/{league_id_uww}").json()
    # get nested dict of scoring settings and tranpsose using .T
    scoring_df_freedom = pd.DataFrame.from_dict(scoring_data_freedom["scoring_settings"], orient="index").T
    scoring_df_uww = pd.DataFrame.from_dict(scoring_data_uww["scoring_settings"], orient="index").T

    return scoring_df_freedom, scoring_df_uww
