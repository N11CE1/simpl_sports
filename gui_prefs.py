from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from prefs import user_preferences
import labels
import buttons
import prefs


def set_sport(checked, key):
    if checked:
        user_preferences.sports_enabled[key] = True
        print(user_preferences.sports_enabled)
        print(user_preferences.sports_enabled[key])
    else:
        user_preferences.sports_enabled[key] = False
        print(user_preferences.sports_enabled)
        print(user_preferences.sports_enabled[key])


def save_sport_num():
    pass


def sport_select():
    container = QWidget()
    sports_grid = QGridLayout()
    sports_grid.setContentsMargins(100, 100, 100, 100)

    nba_label = buttons.sports_button("NBA", action=lambda checked: set_sport(checked, "nba"))
    nfl_label = buttons.sports_button("NFL", action=lambda checked: set_sport(checked, "nfl"))
    nhl_label = buttons.sports_button("NHL", action=lambda checked: set_sport(checked, "nhl"))
    epl_label = buttons.sports_button("EPL", action=lambda checked: set_sport(checked, "epl"))

    sports_grid.addWidget(nba_label, 0, 0)
    sports_grid.addWidget(nfl_label, 0, 1)
    sports_grid.addWidget(nhl_label, 1, 0)
    sports_grid.addWidget(epl_label, 1, 1)

    container.setLayout(sports_grid)

    return container


def preferences_page1(clear_action):
    central_widget = QWidget()
    main_layout = QVBoxLayout(central_widget)

    sports_widget = sport_select()
    question = labels.large_text_label("What sports do you want to follow?")
    main_layout.addWidget(question)
    main_layout.addWidget(sports_widget)

    next_button = buttons.push_button("Next", clear_action)
    main_layout.addWidget(next_button, alignment=Qt.AlignRight)

    return central_widget
