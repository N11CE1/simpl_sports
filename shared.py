sport_list = {"nba": False,
              "nfl": False,
              "nhl": False,
              "epl": False}
sport_order = {i: key for i, key in enumerate(key for key, value in sport_list.items() if value)}


class Prefs:
    def __init__(self,
                 sports_enabled=None,
                 sports_num=None):
        self.sports_enabled = sports_enabled if sports_enabled is not None else sport_list.copy()
        self.sports_order = sports_num if sports_num is not None else {
            i: key for i, key in enumerate(key for key, value in sport_list.items() if value)
        }
        self.spoilers = False


user_preferences = Prefs()

default_prefs = Prefs(
        {"nba": False,
         "nfl": False,
         "nhl": False,
         "epl": False}, {0: "nba", 1: "nfl", 2: "nhl", 3: "epl"})
