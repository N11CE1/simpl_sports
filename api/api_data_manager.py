import time
from api import api_handler as ah
from api import api_constants as ac
import pandas as pd
from datetime import datetime
import pytz

game_status = {
    "scheduled": "Scheduled",
    "created": "Created",
    "inprogress": "In Progress",
    "halftime": "Half-time",
    "complete": "Complete",
    "closed": "Closed",
    "cancelled": "Cancelled",
    "delayed": "Delayed",
    "postponed": "Postponed",
    "time-tbd": "Time-TBD",
    "if-necessary": "If Necessary",
    "unnecessary": "Unnecessary"
}

env = "test" # This is for switching the environment from test to live

## Utility Functions
def find_items(data, target_key):
    """
    Recursively find all the lists associated with the given key, and return the individual items as dictionaries.
    :param data: The JSON data (dictionary or list)
    :param target_key: The key to search for
    :return: A list of dictionaries where each dictionary is an individual item in the "items" list
    """
    items = []

    if isinstance(data, dict):
        # If the data is a dictionary, check if the key exists
        for key, value in data.items():
            if key == target_key and isinstance(value, list):
                # If the key is found and the value is a list, iterate through the list and add to items
                for item in value:
                    if isinstance(item, dict):
                        items.append(item)  # Add each item as a separate dictionary
            # Recur for the value if it's a dictionary or list
            elif isinstance(value, (dict, list)):
                items.extend(find_items(value, target_key))

    elif isinstance(data, list):
        # If the data is a list, iterate over each element
        for item in data:
            items.extend(find_items(item, target_key))

    return items

# Data Transformation or Processing
def get_teams_dataset(league):
    df = pd.DataFrame()
    teams = ah.get_sportsdb_teams_in_league(league)
    df_api = pd.json_normalize(teams, 'teams', sep='_')
    df['short_name'] = df_api['strTeamShort']
    df['name'] = df_api['strTeam']
    df['badge'] = df_api['strBadge']
    df['sport'] = df_api['strSport']
    df['sportsdb_id'] = league

    return df

def get_team_logo(url):
    image_data = ah.get_sportsdb_team_image(url)
    return image_data

def scheduled_games(sport):
    games = {}
    games_data = {}

    # ## Uncomment for production
    # games_data = ah.get_scheduled_games(get_current_est(), sport)

    ## Refactor after dev , condition for testing env only, delete after testing
    if env == "live":
        games_data = ah.get_scheduled_games(get_current_est(), sport)

    else:
        import json
        import os
        current_directory = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(os.path.join(current_directory, r"unit test json")) and os.path.isdir(os.path.join(current_directory, r"unit test json")):
            if sport == ac.app_leagues[0]:
                json_file_path = os.path.join(current_directory, r"unit test json/nba_schedule_24th.json")
            elif sport == ac.app_leagues[1]:
                json_file_path = os.path.join(current_directory, r"unit test json/nfl_schedule_22-26.json")
            elif sport == ac.app_leagues[2]:
                json_file_path = os.path.join(current_directory, r"unit test json/nhl_schedule_25th.json")
            elif sport == ac.app_leagues[3]:
                json_file_path = ''
            else:
                json_file_path = ''

            if json_file_path == '':
                return

            with open(json_file_path, 'r') as file:
                games_data = json.load(file)

    ## End of dev env
    if games_data is not None:
        if sport in (ac.app_leagues[0], ac.app_leagues[2]):
            game_id = None
            date = None
            home = None
            home_team_id = None
            home_alias = None
            home_name = None
            home_score = None
            away = None
            away_team_id = None
            away_alias = None
            away_name = None
            away_score = None
            status = None
            idx = 0
            for game in games_data.get('games', []):
                game_id = game.get('id', None)
                date = game.get('scheduled', None)
                if date is not None:
                    date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
                home = game.get('home', None)

                if home is not None:
                    home_team_id = home.get('id', None)
                    home_alias = home.get('alias', None)
                    home_name = home.get('name', None)
                    home_score = game.get('home_points', 0)

                away = game.get('away', None)
                if away is not None:
                    away_team_id = away.get('id', None)
                    away_alias = away.get('alias', None)
                    away_name = away.get('name', None)
                    away_score = game.get('away_points', 0)
                status = game.get('status', None)

                if status in game_status:
                    status = game_status[status]
                else:
                    status = None

                games[idx] = {
                    'game_id': game_id,
                    'date': date,
                    'home_team_id': home_team_id,
                    'home': home_alias,
                    'home_name': home_name,
                    'home_score': str(home_score),
                    'away_team_id': away_team_id,
                    'away': away_alias,
                    'away_name': away_name,
                    'away_score': str(away_score),
                    'status': status
                }
                idx += 1
        else:
            idx = 0
            week = games_data.get('week', None)
            if week is not None:
                for game in week.get('games', []):
                    game_id = game.get('id', None)
                    date = game.get('scheduled', None)
                    if date is not None:
                        date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
                    home = game.get('home', None)
                    home_team_id = home.get('id', None)
                    home_alias = home.get('alias', None)
                    home_name = home.get('name', None)
                    away = game.get('away', None)
                    away_team_id = away.get('id', None)
                    away_alias = away.get('alias', None)
                    away_name = away.get('name', None)
                    status = game.get('status', None)

                    if status in game_status:
                        status = game_status[status]
                    else:
                        status = None

                    scoring = game.get('scoring', None)
                    home_score = scoring['home_points'] if scoring is not None else 0
                    away_score = scoring['away_points'] if scoring is not None else 0

                    games[idx] = {
                        'game_id': game_id,
                        'date': date,
                        'home_team_id': home_team_id,
                        'home': home_alias,
                        'home_name': home_name,
                        'home_score': str(home_score),
                        'away_team_id': away_team_id,
                        'away': away_alias,
                        'away_name': away_name,
                        'away_score': str(away_score),
                        'status': status
                    }
                    idx += 1

    if len(games) == 0:
        games = None

    return games


def game_box_score(game_id, sport):
    box_score = {}
    box_score_data = {}

    ## uncomment for production
    # box_score_data = ah.get_nba_game_box_score(game_id)

    ## Refactor after dev , condition for testing env only, delete after testing env
    if env == "live":

        box_score_data = ah.get_game_box_score(game_id, sport)

    else:
        import json
        import os
        current_directory = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(os.path.join(current_directory, r"unit test json")) and os.path.isdir(
                os.path.join(current_directory, r"unit test json")):

            if sport == ac.app_leagues[0]:
                json_file_path = os.path.join(current_directory, r"unit test json/nba_box_score.json")
            elif sport == ac.app_leagues[1]:
                json_file_path = os.path.join(current_directory, r"unit test json/nfl_box_score.json")
            elif sport == ac.app_leagues[2]:
                json_file_path = os.path.join(current_directory, r"unit test json/nhl_box_score.json")
            elif sport == ac.app_leagues[3]:
                json_file_path = ''
            else:
                json_file_path = ''

            if json_file_path == '':
                return

            with open(json_file_path, 'r') as file:
                box_score_data = json.load(file)

    ## End of test dev env

    if box_score_data:
        if sport in (ac.app_leagues[0], ac.app_leagues[2]):
            date = None
            home_team_id = None
            home_alias = None
            home_name = None
            home_score = '0'
            home_leaders = None
            away_team_id = None
            away_alias = None
            away_name = None
            away_score = '0'
            away_leaders = None
            status = None

            status = box_score_data.get('status', None)
            if status in game_status:
                status = game_status[status]
            else:
                status = None
            date = box_score_data.get('scheduled', None)
            if date is not None:
                date = datetime.fromisoformat(date).strftime('%Y/%m/%d')

            home = box_score_data.get('home', None)
            away = box_score_data.get('away', None)

            if home is not None:
                home_score = home['points'] if 'points' in home else 0
                home_leaders = home.get('leaders', None)

            if away is not None:
                away_score = away['points'] if 'points' in away else 0
                away_leaders = away.get('leaders', None)

            if sport == ac.app_leagues[0]:
                if home is not None:
                    home_team_id = home['id'] if 'id' in home else None
                    home_alias = home['alias'] if 'alias' in home else None
                    home_name = home['name'] if 'name' in home else None

                if away is not None:
                    away_team_id = away['id'] if 'id' in away else None
                    away_alias = away['alias'] if 'alias' in away else None
                    away_name = away['name'] if 'name' in away else None

            elif sport == ac.app_leagues[2]:
                if home is not None:
                    home_team_id = home['id'] if 'id' in home else None
                    home_name = home["market"] + " " + home['name'] if 'market' in home and 'name' in home else None
                    home_alias = None

                if away is not None:
                    away_team_id = away['id'] if 'id' in away else None
                    away_name = away["market"] + " " + away['name'] if 'market' in away and 'name' in away else None
                    away_alias = None

                # if away is not None:

            home_leader_boards = {}
            away_leader_boards = {}

            if home_leaders is not None:
                if sport == ac.app_leagues[0]:
                    i = 0
                    if "points" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['points']:
                            if 'full_name' in player:
                                key = "name"
                                new_value = player['full_name']
                                add_new = True
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "rebounds" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['rebounds']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "assists" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['assists']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                elif sport == ac.app_leagues[2]:
                    i = 0
                    if "points" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['points']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "goals" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['goals']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "assists" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['assists']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

            if away_leaders is not None:
                if sport == ac.app_leagues[0]:
                    if "points" in box_score_data['away']['leaders']:
                        i = 0
                        for player in box_score_data['away']['leaders']['points']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                        for player in box_score_data['away']['leaders']['rebounds']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                        for player in box_score_data['away']['leaders']['assists']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if "statistics" in player:
                                        stat = player['statistics']
                                        points = stat['points'] if 'points' in stat else 0
                                        rebounds = stat['rebounds'] if 'rebounds' in stat else 0
                                        assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                elif sport == ac.app_leagues[2]:
                    i = 0
                    if "points" in box_score_data['away']['leaders']:
                        for player in box_score_data['away']['leaders']['points']:
                            if "full_name" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "goals" in box_score_data['away']['leaders']:
                        for player in box_score_data['away']['leaders']['goals']:
                            if "statistics" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

                    if "assists" in box_score_data['away']['leaders']:
                        for player in box_score_data['away']['leaders']['assists']:
                            if "statistics" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in away_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(away_leader_boards) == 0:
                                    points = 0
                                    rebounds = 0
                                    assists = 0
                                    if 'statistics' in player:
                                        if 'total' in player['statistics']:
                                            if 'points' in player['statistics']['total']:
                                                stat = player['statistics']['total']
                                                points = stat['points'] if 'points' in stat else 0
                                                rebounds = stat['goals'] if 'goals' in stat else 0
                                                assists = stat['assists'] if 'assists' in stat else 0

                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(points),
                                        'rebounds': str(rebounds),
                                        'assists': str(assists)
                                    }
                                    i += 1

            box_score = {
                "date": date,
                "home_team_id": home_team_id,
                "home": home_alias,
                "home_name": home_name,
                "home_score": str(home_score),
                "home_leader_boards": home_leader_boards,
                "away_team_id": away_team_id,
                "away": away_alias,
                "away_name": away_name,
                "away_score": str(away_score),
                "away_leader_boards": away_leader_boards,
                "status": status
            }

        elif sport == ac.app_leagues[1]:
            date = None
            home_team_id = None
            home_alias = None
            home_name = None
            home_score = '0'
            away_team_id = None
            away_alias = None
            away_name = None
            away_score = '0'
            status = None

            status = box_score_data.get('status', None)
            if status in game_status:
                status = game_status[status]

            date = box_score_data.get('scheduled', None)
            if date is not None:
                date = datetime.fromisoformat(str(date)).strftime('%Y/%m/%d')

            summary = box_score_data.get('summary', None)

            if summary is not None:
                home = summary.get("home", None)
                if home is not None:
                    home_team_id = home['id'] if 'id' in home else None
                    home_alias = home['alias'] if 'alias' in home else None
                    home_name = home["market"] + " " + home['name'] if len(home) > 0 and 'market' in home else None
                    home_score = home['points'] if "points" in home else 0

                away = summary.get("away", None)
                if away is not None:
                    away_team_id = away['id'] if 'id' in away else None
                    away_alias = away['alias'] if len(away) > 0 and 'alias' in away else None
                    away_name = away["market"] + " " + away['name'] if len(away) > 0 and 'market' in away else None
                    away_score = away['points'] if "points" in away else 0

            box_score = {
                "date": date,
                "home_team_id": home_team_id,
                "home": home_alias,
                "home_name": home_name,
                "home_score": str(home_score),
                "home_leader_boards": None,
                "away_team_id": away_team_id,
                "away": away_alias,
                "away_name": away_name,
                "away_score": str(away_score),
                "away_leader_boards": None,
                "status": status
            }

    if len(box_score) == 0:
        box_score = None

    return box_score

game_box_score("","NHL")

def get_standings(sport):
    standings = {}
    standings_data = {}
    current_date = datetime.strptime(get_current_est(), "%Y/%m/%d")
    # ## Uncomment for production
    # standings_data = ah.get_standings(sport, 2024, "REG")

    ## Refactor after dev , condition for testing env only, delete after testing
    if env == "live":
        standings_data = ah.get_standings(sport, current_date.year, "REG")
        # standings_data = ah.get_scheduled_games("2024/11/27", sport)
    else:
        import json
        import os
        current_directory = os.path.dirname(os.path.realpath(__file__))

        if os.path.exists(os.path.join(current_directory, r"unit test json")) and os.path.isdir(
                os.path.join(current_directory, r"unit test json")):
            if sport == ac.app_leagues[0]:
                json_file_path = os.path.join(current_directory, r"unit test json/nba_standings.json")
            elif sport == ac.app_leagues[1]:
                json_file_path = os.path.join(current_directory, r"unit test json/nfl_standings.json")
            elif sport == ac.app_leagues[2]:
                json_file_path = os.path.join(current_directory, r"unit test json/nhl_standings.json")
            elif sport == ac.app_leagues[3]:
                json_file_path = ''
            else:
                json_file_path = ''

            if json_file_path == '':
                return

            with open(json_file_path, 'r') as file:
                standings_data = json.load(file)


    team_stats = {}

    target_key = 'teams'
    teams = find_items(standings_data, target_key)

    idx = 0
    for team in teams:
        team_stats[idx] = {
            "id": team['id'] if 'id' in team else None,
            "name": team['market'] if 'market' in team else "" +  team['name'] if 'name' in team else "",
            "wins": team['wins'] if 'wins' in team else 0,
            "losses": team['losses'] if 'losses' in team else 0,
            "win_pct": team['win_pct'] if 'win_pct' in team else 0,
            "points_for": team['points_for'] if 'points_for' in team else 0,
            "points_against": team['points_against'] if 'points_against' in team else 0,
            "point_diff": team['point_diff'] if 'point_diff' in team else 0
        }
        idx += 1

    return team_stats

def get_current_est():
    est = pytz.timezone('US/Eastern')

    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    est_date = est_now.strftime('%Y/%m/%d')

    return est_date