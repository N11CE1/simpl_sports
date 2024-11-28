from PyQt5.QtWidgets import QWidget, QGridLayout

from buttons.sports_button import SportsButton as SportsButton
from common.shared import user_preferences as user_preferences

MARGIN_SIZE = 100
SPORTS_AND_POSITIONS = [
    ("nba", "NBA", (0, 0)),
    ("nfl", "NFL", (0, 1)),
    ("nhl", "NHL", (1, 0)),
    ("epl", "EPL", (1, 1))
]


def set_sport(checked, key):
    user_preferences.sports_enabled[key] = checked
    print(user_preferences.sports_enabled)


def sport_select():
    container = QWidget()
    sports_grid = QGridLayout()
    sports_grid.setContentsMargins(MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)

    for sport_key, sport_name, position in SPORTS_AND_POSITIONS:
        add_sport_button(sports_grid, sport_key, sport_name, position)

    container.setLayout(sports_grid)
    return container


def add_sport_button(sports_grid, sport_key, sport_name, position):
    action = lambda checked: set_sport(checked, sport_key)
    # print(sport_key)
    sport_button = SportsButton(sport_key, sport_name, action, f"images/{sport_key}.png")
    sports_grid.addWidget(sport_button, *position)
