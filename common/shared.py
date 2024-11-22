sport_list = {"nba": False,
              "nfl": False,
              "nhl": False,
              "epl": False}
sport_order = {i: key for i, key in enumerate(key for key, value in sport_list.items() if value)}

spoilers_enabled = False


class Prefs:
    def __init__(self,
                 sports_enabled=None,
                 sports_num=None,
                 spoilers=None):
        self.sports_enabled = sports_enabled if sports_enabled is not None else sport_list.copy()
        self.sports_order = sports_num if sports_num is not None else {
            i: key for i, key in enumerate(key for key, value in sport_list.items() if value)
        }
        self.spoilers = spoilers_enabled


global user_preferences
user_preferences = Prefs()

prefs_existed = True

default_prefs = Prefs(
        {"nba": True,
         "nfl": True,
         "nhl": True,
         "epl": True},
        {0: "nba", 1: "nfl", 2: "nhl", 3: "epl"},
        False)

test_games = {0: {"date": "16/11/2024",
                  "home": "Giants",
                  "home_score": "50",
                  "away": "Jets",
                  "away_score": "30",
                  "time": "Full Time"
                  },
              1: {"date": "17/11/2024",
                  "home": "Cowboys",
                  "home_score": "10",
                  "away": "Cows",
                  "away_score": "5",
                  "time": "Full Time"
                  },
              2: {"date": "18/11/2024",
                  "home": "Cats",
                  "home_score": "999",
                  "away": "Dogs",
                  "away_score": "1",
                  "time": "Full Time"
                  },
              3: {"date": "19/11/2024",
                  "home": "Wildcats",
                  "home_score": "0",
                  "away": "Wildcats",
                  "away_score": "0",
                  "time": "Full Time"
                  },
              4: {"date": "19/11/2024",
                  "home": "Wildcats",
                  "home_score": "0",
                  "away": "Wildcats",
                  "away_score": "0",
                  "time": "Full Time"
                  },
              5: {"date": "19/11/2024",
                  "home": "Wildcats",
                  "home_score": "0",
                  "away": "Wildcats",
                  "away_score": "0",
                  "time": "Full Time"
                  },
              6: {"date": "19/11/2024",
                  "home": "Wildcats",
                  "home_score": "0",
                  "away": "Wildcats",
                  "away_score": "0",
                  "time": "Full Time"
                  },
              7: {"date": "19/11/2024",
                  "home": "Wildcats",
                  "home_score": "0",
                  "away": "Wildcats",
                  "away_score": "0",
                  "time": "Full Time"
                  }
              }