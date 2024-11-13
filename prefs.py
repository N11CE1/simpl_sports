import configparser
import os


PREFS_FILE = "user_prefs.ini"


class Prefs:
    def __init__(self, sports_enabled, sports_num, spoilers):
        self.sports_enabled = sports_enabled
        self.sports_order = sports_num
        self.spoilers = spoilers


def write_prefs():
    config = configparser.ConfigParser()

    config["sports_enabled"] = {key: str(value).lower() for key, value in user_preferences.sports_enabled.items()}
    config["sports_order"] = {key: str(value).lower() for key, value in user_preferences.sports_order.items()}
    config["spoilers"] = {"spoilers_enabled": str(user_preferences.spoilers).lower()}

    with open(PREFS_FILE, "w") as configfile:
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
    default_sports_enabled = {
        "nba": False,
        "nfl": False,
        "nhl": False,
        "epl": False
    }
    default_sports_order = {key: index + 1 for index, key in enumerate(default_sports_enabled) if
                            default_sports_enabled[key]}
    default_spoilers = False

    if not os.path.exists(PREFS_FILE):
        global user_preferences
        user_preferences = Prefs(default_sports_enabled, default_sports_order,default_spoilers)
        write_prefs()
        print(f"Preferences file {PREFS_FILE} created")
        return read_prefs()
    else:
        returnable = read_prefs()
        print("Preferences loaded successfully.")
        return returnable


def write_on_exit():
    print("Saving preferences...")
    write_prefs()


def get_sports_num():
    return sum(value is True for value in user_preferences.sports_enabled.values()) + 1


user_preferences = check_prefs()
