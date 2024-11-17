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
