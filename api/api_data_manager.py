from PyQt5.QtWidgets import QLabel

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

env = "test"

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
                json_file_path = os.path.join(current_directory, r"unit test json\nba_schedule_24th.json")
            elif sport == ac.app_leagues[1]:
                json_file_path = os.path.join(current_directory, r"unit test json\nfl_schedule_22-26.json")
            elif sport == ac.app_leagues[2]:
                json_file_path = os.path.join(current_directory, r"unit test json\nhl_schedule_25th.json")
            elif sport == ac.app_leagues[3]:
                json_file_path = ''
            else:
                json_file_path = ''

            if json_file_path == '':
                return

            with open(json_file_path, 'r') as file:
                games_data = json.load(file)

    ## End of dev env
    if sport in (ac.app_leagues[0], ac.app_leagues[2]):
        idx = 0
        for game in games_data.get('games', []):
            game_id = game.get('id', None)
            date = game.get('scheduled', None)
            if date is not None:
                date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
            home = game.get('home', None)
            home_alias = home.get('alias', None)
            home_score = game.get('home_points', 0)
            away = game.get('away', None)
            away_alias = away.get('alias', None)
            away_score = game.get('away_points', 0)
            status = game.get('status', None)

            if status in game_status:
                status = game_status[status]
            else:
                status = None

            games[idx] = {
                'game_id': game_id,
                'date': date,
                'home': home_alias,
                'home_score': str(home_score),
                'away': away_alias,
                'away_score': str(away_score),
                'status': status
            }
            idx += 1
    else:
        idx = 0
        week = games_data.get('week', None)
        for game in week.get('games', []):
            game_id = game.get('id', None)
            date = game.get('scheduled', None)
            if date is not None:
                date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
            home = game.get('home', None)
            home_alias = home.get('alias', None)
            away = game.get('away', None)
            away_alias = away.get('alias', None)
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
                'home': home_alias,
                'home_score': str(home_score),
                'away': away_alias,
                'away_score': str(away_score),
                'status': status
            }
            idx += 1

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
                json_file_path = os.path.join(current_directory, r"unit test json\nba_box_score.json")
            elif sport == ac.app_leagues[1]:
                json_file_path = os.path.join(current_directory, r"unit test json\nfl_box_score.json")
            elif sport == ac.app_leagues[2]:
                json_file_path = os.path.join(current_directory, r"unit test json\nhl_box_score.json")
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
            home_score = home['points'] if len(home) > 0 else 0
            away_score = away['points'] if len(away) > 0 else 0
            home_leaders = home.get('leaders', None)
            away_leaders = away.get('leaders', None)

            if sport == ac.app_leagues[0]:
                home_alias = home['alias'] if len(home) > 0 else None
                away_alias = away['alias'] if len(away) > 0 else None
            elif sport in (ac.app_leagues[1], ac.app_leagues[2]):
                home_alias = home["market"] + " " + home['name'] if len(home) > 0 else None
                away_alias = away["market"] + " " + away['name'] if len(away) > 0 else None

            home_leader_boards = {}
            away_leader_boards = {}

            if home_leaders is not None:
                if sport == ac.app_leagues[0]:
                    i = 0
                    if "points" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['points']:
                            if "statistics" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']
                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

                    if "rebounds" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['rebounds']:
                            if "statistics" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']

                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

                    if "assists" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['assists']:
                            if "statistics" in player:
                                add_new = True
                                key = "name"
                                new_value = player['full_name']

                                for outer_key, inner_dict in home_leader_boards.items():
                                    for inner_key, value in inner_dict.items():
                                        if inner_key == key and value == new_value:
                                            add_new = False
                                            break

                                if add_new or len(home_leader_boards) == 0:
                                    home_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

                elif sport == ac.app_leagues[2]:
                    i = 0
                    if "points" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['points']:
                            if "statistics" in player:
                                    add_new = True
                                    key = "name"
                                    new_value = player['full_name']
                                    for outer_key, inner_dict in home_leader_boards.items():
                                        for inner_key, value in inner_dict.items():
                                            if inner_key == key and value == new_value:
                                                add_new = False
                                                break

                                    if add_new or len(home_leader_boards) == 0:
                                        home_leader_boards[i] = {
                                            'name': player['full_name'],
                                            'points': str(player["statistics"]["total"]["points"]),
                                            'rebounds': str(player["statistics"]["total"]["goals"]),
                                            'assists': str(player["statistics"]["total"]["assists"])
                                        }
                                        i += 1

                    if "goals" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['goals']:
                            if "statistics" in player:
                                    add_new = True
                                    key = "name"
                                    new_value = player['full_name']
                                    for outer_key, inner_dict in home_leader_boards.items():
                                        for inner_key, value in inner_dict.items():
                                            if inner_key == key and value == new_value:
                                                add_new = False
                                                break

                                    if add_new or len(home_leader_boards) == 0:
                                        home_leader_boards[i] = {
                                            'name': player['full_name'],
                                            'points': str(player["statistics"]["total"]["points"]),
                                            'rebounds': str(player["statistics"]["total"]["goals"]),
                                            'assists': str(player["statistics"]["total"]["assists"])
                                        }
                                        i += 1

                    if "assists" in box_score_data['home']['leaders']:
                        for player in box_score_data['home']['leaders']['assists']:
                            if "statistics" in player:
                                    add_new = True
                                    key = "name"
                                    new_value = player['full_name']
                                    for outer_key, inner_dict in home_leader_boards.items():
                                        for inner_key, value in inner_dict.items():
                                            if inner_key == key and value == new_value:
                                                add_new = False
                                                break

                                    if add_new or len(home_leader_boards) == 0:
                                        home_leader_boards[i] = {
                                            'name': player['full_name'],
                                            'points': str(player["statistics"]["total"]["points"]),
                                            'rebounds': str(player["statistics"]["total"]["goals"]),
                                            'assists': str(player["statistics"]["total"]["assists"])
                                        }
                                        i += 1

            if away_leaders is not None:
                if sport == ac.app_leagues[0]:
                    if "points" in box_score_data['away']['leaders']:
                        i = 0
                        for player in box_score_data['away']['leaders']['points']:
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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

                        for player in box_score_data['away']['leaders']['rebounds']:
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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player['statistics']['points']),
                                        'rebounds': str(player['statistics']['rebounds']),
                                        'assists': str(player['statistics']['assists'])
                                    }
                                    i += 1

                elif sport == ac.app_leagues[2]:
                    i = 0
                    if "points" in box_score_data['away']['leaders']:
                        for player in box_score_data['away']['leaders']['points']:
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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player["statistics"]["total"]["points"]),
                                        'rebounds': str(player["statistics"]["total"]["goals"]),
                                        'assists': str(player["statistics"]["total"]["assists"])
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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player["statistics"]["total"]["points"]),
                                        'rebounds': str(player["statistics"]["total"]["goals"]),
                                        'assists': str(player["statistics"]["total"]["assists"])
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
                                    away_leader_boards[i] = {
                                        'name': player['full_name'],
                                        'points': str(player["statistics"]["total"]["points"]),
                                        'rebounds': str(player["statistics"]["total"]["goals"]),
                                        'assists': str(player["statistics"]["total"]["assists"])
                                    }
                                    i += 1

            box_score = {
                "date": date,
                "home": home_alias,
                "home_score": home_score,
                "home_leader_boards": home_leader_boards,
                "away": away_alias,
                "away_score": away_score,
                "away_leader_boards": away_leader_boards,
                "status": status
            }

        elif sport == ac.app_leagues[1]:
            status = box_score_data.get('status', None)
            if status in game_status:
                status = game_status[status]
            else:
                status = None
            date = box_score_data.get('scheduled', None)
            if date is not None:
                date = datetime.fromisoformat(date).strftime('%Y/%m/%d')

            summary = box_score_data.get('summary', None)
            if summary is not None:
                home = summary["home"]
                away = summary["away"]
                home_alias = home["market"] + " " + home['name'] if len(home) > 0 else None
                away_alias = away["market"] + " " + away['name'] if len(away) > 0 else None
                home_score = home["points"]
                away_score = away["points"]

            box_score = {
                "date": date,
                "home": home_alias,
                "home_score": home_score,
                "home_leader_boards": None,
                "away": away_alias,
                "away_score": away_score,
                "away_leader_boards": None,
                "status": status
            }

    if len(box_score) == 0:
        box_score = None

    return box_score

def get_current_est():
    # Get the EST timezone object
    est = pytz.timezone('US/Eastern')

    # Get the current time in UTC, then convert to EST
    utc_now = datetime.now(pytz.utc)
    est_now = utc_now.astimezone(est)
    est_date = est_now.strftime('%Y/%m/%d')

    return est_date
