import configparser
import os

PREFS_FILE = "user_prefs.ini"


class Prefs:
    def __init__(self, sports_enabled, sports_num, spoilers):
        self.sports_enabled = sports_enabled
        self.sports_order = sports_num
        self.spoilers = spoilers


def write_prefs():
    prefs_file = "user_prefs.ini"

    config = configparser.ConfigParser()

    sports_dict = {"nba": True,
                   "nfl": True,
                   "nhl": True,
                   "epl": True
                   }

    config["sports_enabled"] = {key: str(value).lower() for key, value in sports_dict.items()}

    sports_order = {key: value for key, value in sports_dict.items() if value}
    sports_order = {key: index + 1 for index, key in enumerate(sports_order)}

    config["sports_order"] = {key: str(value).lower() for key, value in sports_order.items()}

    spoilers_section = "spoilers"
    key_name = "spoilers_enabled"
    default_value = "false"

    config.add_section(spoilers_section)
    config.set(spoilers_section, key_name, default_value)

    with open(prefs_file, "w") as configfile:
        config.write(configfile)


def read_prefs():
    config = configparser.ConfigParser()
    config.read("user_prefs.ini")

    sports = config["sports_enabled"]
    sports_dict = {key: sports.getboolean(key) for key in sports}
    print(sports_dict)

    sports_order = config["sports_order"]
    sports_order_dict = {key: sports_order.getint(key) for key in sports_order}
    print(sports_order_dict)

    spoilers_enabled = config.getboolean('spoilers', 'spoilers_enabled')
    print(f"Spoilers Enabled: {spoilers_enabled}")

    return Prefs(sports_dict, sports_order_dict, spoilers_enabled)


def check_prefs():
    if not os.path.exists(PREFS_FILE):
        write_prefs()
        print(f"Preferences file {PREFS_FILE} created")
        return read_prefs()
    else:
        returnable = read_prefs()
        print("Preferences loaded successfully.")
        return returnable


def get_sports_num():
    return sum(value is True for value in user_preferences.sports_enabled.values()) + 1


user_preferences = check_prefs()
