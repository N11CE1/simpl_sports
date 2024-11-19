import requests as req
import json as js
import pandas as pd
import api_handler as ah
import api_constants as ac
import datasets
import api_data_manager as adm
import data_operations as do

def try_sportscore():
	response = req.get(ac.sportscore_base_url, headers=ac.sportscore_headers)
	print(response.status_code)
	print(response.json())

def try_sports_db():
	teams = ah.get_teams_in_league(ac.sportsdb_leagues[3])
	df = pd.json_normalize(teams, 'teams', sep='_')
	print(df[['strTeamShort','strTeam','strSport','strBadge']])

df = adm.get_teams_dataset(ac.sportsdb_leagues[3])

do.save_team_info(df, ac.sportsdb_leagues[3])


