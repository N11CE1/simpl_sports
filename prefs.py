import configparser
import os

import shared
from shared import user_preferences


PREFS_FILE = "user_prefs.ini"


def write_prefs(preferences):
    config = configparser.ConfigParser()

    config["sports_enabled"] = {key: str(value).lower() for key, value in preferences.sports_enabled.items()}
    config["sports_order"] = {str(key): value for key, value in preferences.sports_order.items()}
    config["spoilers"] = {"spoilers_enabled": str(preferences.spoilers).lower()}

    with open(PREFS_FILE, "w") as configfile:
        config.write(configfile)


def read_prefs():
    config = configparser.ConfigParser()
    config.read("user_prefs.ini")

    sports_enabled = {key: config.getboolean("sports_enabled", key) for key in config["sports_enabled"]}
    print(sports_enabled)

    # sports_order = dict(config["sports_order"])
    sports_order = {key: config.get("sports_order", key) for key in config["sports_order"]}
    print(sports_order)

    spoilers_enabled = config.getboolean('spoilers', 'spoilers_enabled')
    print(f"Spoilers Enabled: {spoilers_enabled}")

    user_preferences.sports_enabled = sports_enabled
    user_preferences.sports_order = sports_order
    user_preferences.spoilers = spoilers_enabled
    return user_preferences


def check_prefs():
    if not os.path.exists(PREFS_FILE):
        shared.prefs_existed = False
        write_prefs(user_preferences)
        print(f"Preferences file {PREFS_FILE} created")
        return read_prefs()
    else:
        returnable = read_prefs()
        print("Preferences loaded successfully.")
        return returnable


def write_on_exit(preferences):
    print("Saving preferences...")
    write_prefs(preferences)
