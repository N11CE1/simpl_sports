import api_handler as ah
import api_constants as ac
import pandas as pd
import datasets


# Data Transformation or Processing
def parse_api_response(response): # Parses the raw JSON or XML response from the API into a usable format (dict, list, etc.).
    pass

def get_teams_dataset(league):
    df = pd.DataFrame()
    if league == ac.sportsdb_leagues[3]:
        teams = ah.get_teams_in_league(ac.sportsdb_leagues[3])
        df_api = pd.json_normalize(teams, 'teams', sep='_')
        df['short_name'] = df_api['strTeamShort']
        df['name'] = df_api['strTeam']
        df['badge'] = df_api['strBadge']
        df['sport'] = df_api['strSport']
        df['sportsdb_id'] = ac.sportsdb_leagues[3]

    return df
