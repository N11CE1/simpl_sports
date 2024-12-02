# Worker Thread Class
import time
from PyQt5.QtCore import QThread, pyqtSignal
import json
import os

from api import api_constants as ac
from api import data_operations as do
from api import api_data_manager as adm
from api import datasets as da

## Download static data from thesportsdb like League Information
## Team Information including logo
class Initialize_App(QThread):
    running_task = pyqtSignal(str, str, int)
    progress = 0
    def run(self):
        ## Download league information
        if len(ac.sportsdb_leagues) > 0:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            json_file_path = os.path.join(current_directory, 'sportsdb_leagues.json')
            with open(json_file_path, 'r') as file:
                league_data = json.load(file)
            leagues = []
            for league in league_data.get("leagues", []):
                short_name = league.get("short_name")
                name = league.get("name")
                badge = league.get("badge")
                badge_image = None
                sportsdb_id = league.get("sportsdb_id")

                new_row = [short_name, name, badge, badge_image, sportsdb_id]
                leagues.append(new_row)
                self.progress += 1
                self.running_task.emit('Downloading league information...', f"Downloaded {name} information.", self.progress)
                time.sleep(.1)
            do.save_league_info(leagues)

        ## Download team information
        if len(ac.sportsdb_leagues) > 0:
            for league in ac.sportsdb_leagues:
                teams = adm.get_teams_dataset(league)
                existing_teams = do.get_league_teams(league)
                if len(existing_teams) == 0:
                    do.save_team_info(teams, league)
                    self.progress += 1
                    self.running_task.emit('Downloading teams information...', f"Downloaded teams of {league}.", self.progress)
                    time.sleep(.1)
                else:
                    print(f"{league} teams already exists!")

        ## Download team logo
        if len(ac.sportsdb_leagues) > 0:
            for league in ac.sportsdb_leagues:
                teams = do.get_league_teams(league)
                if len(teams) > 0:
                    for i in range(len(teams)):
                        team = do.get_team_info(short_name=teams.iloc[i, 0], sportsdb_id=league).head(1)
                        image = adm.get_team_logo(team.loc[0, 'badge'])
                        do.save_image_to_db(image, team.loc[0, 'name'], team.loc[0, 'sportsdb_id'])
                        self.progress += 1
                        self.running_task.emit('Downloading teams information...',
                                                   f"Downloaded logo of {team.loc[0, 'name']} in {team.loc[0, 'sportsdb_id']}.", self.progress)

        time.sleep(2)
        self.progress += 1
        self.running_task.emit('Cleaning up temp files and finishing task...', None, self.progress)
        time.sleep(2)
        self.progress += 1
        self.running_task.emit('Simple Sports is successfully initialized.', None, self.progress)
        time.sleep(2)
        self.progress += 1
        self.running_task.emit('Done', None, self.progress)  # Emit signal when task is done

    def stop(self):
        """Stop the task gracefully"""
        print("Stopping initializer background task...")  # Debugging print
        self.quit()  # Ensure the thread exits gracefully

class Update_Games_Score(QThread):
    update_ui = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.counter = 0
        self._running = True

    def run(self):
        print("Background thread started...")
        while self._running:
            nba_games = adm.scheduled_games("NBA")

            if nba_games is not None:
                da.nba_scheduled_games = nba_games

                games_in_progress = {}
                idx = 0
                for game_key, game in nba_games.items():
                    game_id = game["game_id"]
                    status = game.get("status")
                    date = game.get("date")
                    home_team_id = game.get("home_team_id")
                    home = game.get("home")
                    home_name = game.get("home_name")
                    home_score = game.get("home_score")
                    away_team_id = game.get("away_team_id")
                    away = game.get("away")
                    away_name = game.get("away_name")
                    away_score = game.get("away_score")

                    if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                        games_in_progress[idx] = {
                            "game_id": game_id,
                            "date": date,
                            "home_team_id": home_team_id,
                            "home": home,
                            "home_name": home_name,
                            "home_score": home_score,
                            "home_leader_boards": None,
                            "away_team_id": away_team_id,
                            "away": away,
                            "away_name": away_name,
                            "away_score": away_score,
                            "away_leader_boards": None,
                            "status": status
                        }
                        idx += 1

                da.nba_box_score = games_in_progress

            nfl_games = adm.scheduled_games("NFL")
            if nfl_games is not None:
                da.nfl_scheduled_games = nfl_games

                games_in_progress = {}
                idx = 0
                for game_key, game in nfl_games.items():
                    game_id = game["game_id"]
                    status = game.get("status")
                    date = game.get("date")
                    home_team_id = game.get("home_team_id")
                    home = game.get("home")
                    away_team_id = game.get("away_team_id")
                    away = game.get("away")
                    home_score = game.get("home_score")
                    away_score = game.get("away_score")

                    if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                        games_in_progress[idx] = {
                            "game_id": game_id,
                            "date": date,
                            "home_team_id": home_team_id,
                            "home": home,
                            "home_name": home_name,
                            "home_score": home_score,
                            "home_leader_boards": None,
                            "away_team_id": away_team_id,
                            "away": away,
                            "away_name": away_name,
                            "away_score": away_score,
                            "away_leader_boards": None,
                            "status": status
                        }
                        idx += 1

                da.nfl_box_score = games_in_progress

            nhl_games = adm.scheduled_games("NHL")
            if nhl_games is not None:
                da.nhl_scheduled_games = nhl_games

                games_in_progress = {}
                idx = 0
                for game_key, game in nhl_games.items():
                    game_id = game["game_id"]
                    status = game.get("status")
                    date = game.get("date")
                    home_team_id = game.get("home_team_id")
                    home = game.get("home")
                    away_team_id = game.get("away_team_id")
                    away = game.get("away")
                    home_score = game.get("home_score")
                    away_score = game.get("away_score")

                    if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                        games_in_progress[idx] = {
                            "game_id": game_id,
                            "date": date,
                            "home_team_id": home_team_id,
                            "home": home,
                            "home_name": home_name,
                            "home_score": home_score,
                            "home_leader_boards": None,
                            "away_team_id": away_team_id,
                            "away": away,
                            "away_name": away_name,
                            "away_score": away_score,
                            "away_leader_boards": None,
                            "status": status
                        }
                        idx += 1

                da.nhl_box_score = games_in_progress

            ## Game Box Score
            for key, games in da.nba_box_score.items():
                box_score = adm.game_box_score(games["game_id"], ac.app_leagues[0])
                if box_score is not None:
                    games["date"] = box_score["date"]
                    games["home_team_id"] = box_score["home_team_id"]
                    games["home"] = box_score["home"]
                    games["home_name"] = box_score["home_name"]
                    games["home_score"] = box_score["home_score"]
                    games["home_leader_boards"] = box_score["home_leader_boards"]
                    games["away_team_id"] = box_score["away_team_id"]
                    games["away"] = box_score["away"]
                    games["away_name"] = box_score["away_name"]
                    games["away_score"] = box_score["away_score"]
                    games["away_leader_boards"] = box_score["away_leader_boards"]
                    games["status"] = box_score["status"]

            for key, games in da.nfl_box_score.items():
                box_score = adm.game_box_score(games["game_id"], ac.app_leagues[1])
                if box_score is not None:
                    games["date"] = box_score["date"]
                    games["home_team_id"] = box_score["home_team_id"]
                    games["home"] = box_score["home"]
                    games["home_name"] = box_score["home_name"]
                    games["home_score"] = box_score["home_score"]
                    games["home_leader_boards"] = box_score["home_leader_boards"]
                    games["away_team_id"] = box_score["away_team_id"]
                    games["away"] = box_score["away"]
                    games["away_name"] = box_score["away_name"]
                    games["away_score"] = box_score["away_score"]
                    games["away_leader_boards"] = box_score["away_leader_boards"]
                    games["status"] = box_score["status"]

            for key, games in da.nhl_box_score.items():
                box_score = adm.game_box_score(games["game_id"], ac.app_leagues[2])
                if box_score is not None:
                    games["date"] = box_score["date"]
                    games["home_team_id"] = box_score["home_team_id"]
                    games["home"] = box_score["home"]
                    games["home_name"] = box_score["home_name"]
                    games["home_score"] = box_score["home_score"]
                    games["home_leader_boards"] = box_score["home_leader_boards"]
                    games["away_team_id"] = box_score["away_team_id"]
                    games["away"] = box_score["away"]
                    games["away_name"] = box_score["away_name"]
                    games["away_score"] = box_score["away_score"]
                    games["away_leader_boards"] = box_score["away_leader_boards"]
                    games["status"] = box_score["status"]

            ## Standings for Chart
            nba_standings = adm.get_standings(ac.app_leagues[0])
            if nba_standings is not None:
                da.nba_standings = nba_standings

            nfl_standings = adm.get_standings(ac.app_leagues[1])
            if nfl_standings is not None:
                da.nfl_standings = nfl_standings

            nhl_standings = adm.get_standings(ac.app_leagues[2])
            if nhl_standings is not None:
                da.nhl_standings = nhl_standings

            print("API calls done. Background thread is going to sleep for 5 minutes. Good night!")

            self.update_ui.emit()
            time.sleep(3600)

        print("Task stopped!")
        self.sport.emit("Task stopped!")

    def stop(self):
        """Stop the task gracefully"""
        print("Stopping background task...")  # Debugging print
        self._running = False  # Set the running flag to False to stop the loop
        self.quit()  # Ensure the thread exits gracefully