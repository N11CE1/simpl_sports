import pandas as pd
from api import data_operations as do
from api import api_constants as ac
# from api.start_app import teams

# In-memory data for gui widget values
sports = []
leagues = pd.DataFrame()
nba_teams = []

global nba_scheduled_games
global nfl_scheduled_games
global nhl_scheduled_games
global nba_box_score
global nfl_box_score
global nhl_box_score
global nba_standings
global nfl_standings
global nhl_standings

nba_scheduled_games = {}
nfl_scheduled_games = {}
nhl_scheduled_games = {}

nba_box_score = {}
nfl_box_score = {}
nhl_box_score = {}

nba_standings = {}
nhl_standings = {}
nfl_standings = {}


def fill_leagues_dataset():
    global leagues
    leagues = do.get_leagues()

def get_leagues():
    return leagues

def set_global_dataframe():
    """Function to set the global dataframe"""
    global leagues
    leagues = do.get_leagues()

def get_global_dataframe():
    """Function to retrieve the global dataframe"""
    return leagues

def get_static_games(game_id, sport):
    global nba_scheduled_games
    global nfl_scheduled_games
    global nhl_scheduled_games
    games = {}
    box_score = {}
    if sport == ac.app_leagues[0]:
        if len(nba_scheduled_games) > 0:
            games = nba_scheduled_games
    elif sport == ac.app_leagues[1]:
        if len(nfl_scheduled_games) > 0:
            games = nfl_scheduled_games
    elif sport == ac.app_leagues[2]:
        if len(nhl_scheduled_games) > 0:
            games = nhl_scheduled_games

    if len(games) > 0:
        for key, game in games.items():
            if game['game_id'] == game_id:
                box_score = {
                    "date": game["date"],
                    "home": game["home"],
                    "home_name": game["home_name"],
                    "home_score": game["home_score"],
                    "home_leader_boards": None,
                    "away": game["away"],
                    "away_name": game["away_name"],
                    "away_score": game["away_score"],
                    "away_leader_boards": None,
                    "status": game["status"]
                }
                break

    return box_score

def get_box_score(game_id, sport):
    global nba_box_score
    global nfl_box_score
    global nhl_box_score

    games_in_progress = {}
    if sport == ac.app_leagues[0]:
        for key, games in nba_box_score.items():
            games_in_progress = {
                "date": games["date"],
                "home": games["home"],
                "home_name": games["home_name"],
                'home_score': games["home_score"],
                "home_leader_boards": games["home_leader_boards"],
                "away": games["away"],
                "away_name": games["away_name"],
                'away_score': games["away_score"],
                "away_leader_boards": games["away_leader_boards"],
                'status': games["status"]
            }

    elif sport == ac.app_leagues[1]:
        for key, games in nfl_box_score.items():
            games_in_progress = {
                "date": games["date"],
                "home": games["home"],
                "home_name": games["home_name"],
                'home_score': games["home_score"],
                "home_leader_boards": games["home_leader_boards"],
                "away": games["away"],
                "away_name": games["away_name"],
                'away_score': games["away_score"],
                "away_leader_boards": games["away_leader_boards"],
                'status': games["status"]
            }
    elif sport == ac.app_leagues[2]:
        for key, games in nhl_box_score.items():
            games_in_progress = {
                "date": games["date"],
                "home": games["home"],
                "home_name": games["home_name"],
                'home_score': games["home_score"],
                "home_leader_boards": games["home_leader_boards"],
                "away": games["away"],
                "away_name": games["away_name"],
                'away_score': games["away_score"],
                "away_leader_boards": games["away_leader_boards"],
                'status': games["status"]
            }

    if games_in_progress is None:
        return None
    else:
        return games_in_progress

def get_team_stats(team_id, sport):
    global nba_standings
    global nfl_standings
    global nhl_standings

    team_stat = {}
    if sport == ac.app_leagues[0]:
        for key, team in nba_standings.items():
            if team["id"] == team_id:
                team_stat = {
                    "wins": team["wins"],
                    'losses': team["losses"],
                    "win_pct": team["win_pct"],
                    "points_for": team["points_for"],
                    "points_against": team["points_against"],
                    'point_diff': team["point_diff"]
                }
                break
    elif sport == ac.app_leagues[1]:
        for key, team in nfl_standings.items():
            if team["id"] == team_id:
                team_stat = {
                    "wins": team["wins"],
                    'losses': team["losses"],
                    "win_pct": team["win_pct"],
                    "points_for": team["points_for"],
                    "points_against": team["points_against"],
                    'point_diff': team["point_diff"]
                }
                break

    elif sport == ac.app_leagues[2]:
        for key, team in nhl_standings.items():
            if team["id"] == team_id:
                team_stat = {
                    "wins": team["wins"],
                    'losses': team["losses"],
                    "win_pct": team["win_pct"],
                    "points_for": team["points_for"],
                    "points_against": team["points_against"],
                    'point_diff': team["point_diff"]
                }
                break

    return team_stat