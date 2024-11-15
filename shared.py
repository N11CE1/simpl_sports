sport_list = {"nba": False,
              "nfl": False,
              "nhl": False,
              "epl": False}
sport_order = {i: key for i, key in enumerate(key for key, value in sport_list.items() if value)}
class Prefs:
    def __init__(self,
                 sports_enabled=sport_list,
                 sports_num= sport_order,
                 spoilers=False):
        self.sports_enabled = sports_enabled
        self.sports_order = sports_num
        self.spoilers = spoilers


user_preferences = Prefs()
