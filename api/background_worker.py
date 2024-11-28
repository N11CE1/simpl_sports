# Worker Thread Class
import time

from PyQt5.QtCore import QThread, pyqtSignal
import json
import os
from api import api_constants as ac
from api import data_operations as do
from api import api_data_manager as adm

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