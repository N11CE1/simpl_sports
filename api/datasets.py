import pandas as pd
import data_operations as do

# In-memory data for gui widget values
sports = []
leagues = pd.DataFrame()
nba_teams = []

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

from api import api_data_manager as adm

