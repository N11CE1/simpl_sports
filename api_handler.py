import requests as rq
import json as js
import api_constants as ac

# Fetching Sports Data
def get_league_info():
    pass

def get_teams_in_league(league): # API request from thesportsdb
    api_call = rq.get(ac.thesportsdb_base_url + f'search_all_teams.php?l={league}')
    return api_call.json()

def get_live_scores(): # Fetches live scores for ongoing matches.
    pass

def get_team_info(team): # From thesportsdb
    api_call = rq.get(ac.thesportsdb_base_url + f'searchteams.php?sname={team}')
    return js.loads(api_call.json())

# API Request Management
def handle_api_error(response): # Handles API errors (like invalid responses, rate limits, etc.) and provides fallback data or retries.
    pass

# Authentication
def get_api_key(): # Retrieves the API key from a secure location (environment variable, config file).
    pass

def store_api_key(api_key): # Saves the API key for future use.
    pass