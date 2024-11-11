import configparser
import os


def write_prefs():
    prefs_file = "user_prefs.ini"

    config = configparser.ConfigParser()

    sports_dict = {"nba": True,
                   "nfl": True,
                   "nhl": True,
                   "epl": False
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
    # print(sports_dict)
    sports_order = config["sports_order"]
    sports_order_dict = {key: sports_order.getint(key) for key in sports_order}
    # print(sports_order_dict)


write_prefs()
read_prefs()