from io import BytesIO

import requests
import json
from api import api_constants as ac

# Fetching Sports Data
def get_sportsdb_teams_in_league(league):
    api_call = requests.get(ac.thesportsdb_base_url + f'search_all_teams.php?l={league}')
    return api_call.json()

def get_sportsdb_team_info(team):
    api_call = requests.get(ac.thesportsdb_base_url + f'searchteams.php?sname={team}')
    return json.loads(api_call.json())

def get_sportsdb_team_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

def get_scheduled_games(game_date, sport):
    print(f"API call to get scheduled games for {sport}")
    if sport == ac.sportsdb_leagues[0]:
        games_schedule_url = f"{ac.sportradar_base_url}nba/trial/v8/en/games/{game_date}/schedule.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[1]:
        games_schedule_url = f"{ac.sportradar_base_url}nfl/official/trial/v7/en/games/current_week/schedule.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[2]:
        games_schedule_url = f"{ac.sportradar_base_url}nhl/trial/v7/en/games/{game_date}/schedule.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[3]:
        games_schedule_url = ""
    else:
        games_schedule_url = ""

    if not games_schedule_url == "":
        api_call = requests.get(games_schedule_url, headers=ac.sportradar_headers)

        if api_call.status_code == 200:
            return api_call.json()
        else:
            print("Request failed with status code:", api_call.status_code)
            return None
    else:
        print("No API URL was defined.")
        return None

def get_game_box_score(game_id, sport):
    print(f"API call to get box score for game_key:{game_id} sport: {sport}")
    if sport == ac.sportsdb_leagues[0]:
        game_box_score_url = f"{ac.sportradar_base_url}nba/trial/v8/en/games/{game_id}/boxscore.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[1]:
        game_box_score_url = f"{ac.sportradar_base_url}nfl/official/trial/v7/en/games/{game_id}/boxscore.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[2]:
        game_box_score_url = f"{ac.sportradar_base_url}nhl/trial/v7/en/games/{game_id}/boxscore.json?api_key={ac.sportradar_key}"
    elif sport == ac.sportsdb_leagues[3]:
        game_box_score_url = ""
    else:
        game_box_score_url = ""

    api_call = requests.get(game_box_score_url, headers=ac.sportradar_headers)

    if api_call.status_code == 200:
        return api_call.json()
    else:
        print("Request failed with status code:", api_call.status_code)

def get_standings(sport, year, season):
    print(f"API call to get standings for sport: {sport}")
    if sport == ac.sportsdb_leagues[0]:

        standing_url = f"{ac.sportradar_base_url}nba/trial/v8/en/seasons/{year}/{season}/standings.json?api_key={ac.sportradar_key}"

    elif sport == ac.sportsdb_leagues[1]:

        standing_url = f"{ac.sportradar_base_url}/nfl/official/trial/v7/en/seasons/{year}/{season}/standings/season.json?api_key={ac.sportradar_key}"

    elif sport == ac.sportsdb_leagues[2]:

        standing_url = f"{ac.sportradar_base_url}nhl/trial/v7/en/seasons/{year}/{season}/standings.json?api_key={ac.sportradar_key}"

    elif sport == ac.sportsdb_leagues[3]:
        standing_url = ""

    else:
        standing_url = ""

    api_call = requests.get(standing_url, headers=ac.sportradar_headers)

    if api_call.status_code == 200:
        return api_call.json()
    else:
        print("Request failed with status code:", api_call.status_code)
