import time

import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QButtonGroup, QFrame
from streamlit import radio

from buttons.radio_game_button import RadioGameButton
from api import api_data_manager as adm
from api import datasets as da
from api import api_constants as ac
from common.shared import user_preferences
from common import shared
from graph.graph_team_record_analysis import StatsChart

class GameSelection(QWidget):
    game_selected = pyqtSignal(str, str, str, object)
    SCROLL_AREA_STYLE = """
            QScrollArea {
                border: 2px solid #ccc;
                border-radius: 10px;
                background: transparent;
                padding-bottom: 0px;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: transparent;
                border-radius: 4px;
                margin-left: 5px;
                margin-right: 5px;
                margin-bottom: 4px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-height: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #666;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal,
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
            background: transparent;
            background-color: transparent;
            background-image: none;
            border: none;
            width: 0px;
            height: 0px;
            margin: 0px;
            padding: 0px;
            }
            """

    def __init__(self):
        super().__init__()
        self.stat_graph = None
        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        scroll_area.setFixedHeight(189)
        scroll_area.setStyleSheet(self.SCROLL_AREA_STYLE)

        self.main_layout.addWidget(scroll_area)

        container = QWidget(self)
        self.hbox = QHBoxLayout()
        container.setLayout(self.hbox)

        scroll_area.setWidget(container)

        self.games_button_group = QButtonGroup()
        self.games_button_group.setExclusive(True)
        # self.games_button_group.buttonClicked.connect(self.on_button_clicked)

    def update_games(self, sport):
        # print(f"Game Selection updated for sport {sport}")
        if sport is None:
            print("No sport specified")
            return

        while self.hbox.count():
            item = self.hbox.takeAt(0)
            widget = item.widget()
            if widget:
                self.games_button_group.removeButton(widget)
                widget.deleteLater()

        sport_games = None
        if sport == ac.app_leagues[0]:
            sport_games = da.nba_scheduled_games

        elif sport == ac.app_leagues[1]:
            sport_games = da.nfl_scheduled_games

        elif sport == ac.app_leagues[2]:
            sport_games = da.nhl_scheduled_games

        if sport_games is None:
            print(f"No games found for {sport}")
            return

        first_game = None

        for game_key, game in sport_games.items():
            game_id = game["game_id"]
            status = game.get("status")
            date = game.get("date")
            home_team_id = game.get("home_team_id")
            home = game.get("home")
            away_team_id = game.get("away_team_id")
            away = game.get("away")

            home_score = 0
            away_score = 0
            real_home_score = 0
            real_away_score = 0

            if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                box_score = da.get_box_score(game_id, sport)
                if box_score:
                    real_home_score = box_score.get("home_score")
                    real_away_score = box_score.get("away_score")

                    if user_preferences.spoilers:
                        home_score = real_home_score
                        away_score = real_away_score
                    else:
                        home_score = "--"
                        away_score = "--"

            else:
                home_score = game.get("home_score")
                away_score = game.get("away_score")
                real_home_score = home_score
                real_away_score = away_score

            if status is not None:
                radio_button = RadioGameButton(date=date, home=home, home_score=home_score,
                                               away=away, away_score=away_score, time=status)
                radio_button.setProperty("sport", sport)
                radio_button.setProperty("game_key", str(game_id))
                radio_button.setProperty("home_score", str(real_home_score))
                radio_button.setProperty("away_score", str(real_away_score))
                radio_button.setProperty("home_team_id", str(home_team_id))
                radio_button.setProperty("away_team_id", str(away_team_id))

                self.games_button_group.addButton(radio_button)
                self.hbox.addWidget(radio_button)

                radio_button.toggled.connect(self.on_button_toggled)

                # if first_game is None:
                #     first_game = radio_button

        if first_game is not None:

            first_game.setChecked(True)
            game_key = first_game.property("game_key")
            sport = first_game.property("sport")
            status = first_game.time_label.text()
            if game_key is not None and sport is not None:
                # print(f"Default game selected: {game_key}, sport: {sport}")
                self.game_selected.emit(game_key, sport, status)

        if user_preferences.spoilers:
            self.spoiler_toggled(self)

    def on_button_toggled(self, checked):
        if checked:
            button = self.sender()
            game_key = button.property('game_key')
            sport = button.property('sport')
            status = button.time_label.text()
            home_team_id = button.property('home_team_id')
            away_team_id = button.property('away_team_id')
            home_team_name = button.home_label.text()
            away_team_name = button.away_label.text()

            if game_key is not None and sport is not None:
                # Create the StatsChart instance
                df_home_team_stats = da.get_team_stats(home_team_id, sport)
                df_away_team_stats = da.get_team_stats(away_team_id, sport)

                if df_home_team_stats is not None and df_away_team_stats is not None:
                    stat_graph = StatsChart(
                        home_team_name, away_team_name,
                        df_home_team_stats, df_away_team_stats, sport
                    )
                else:
                    stat_graph = None

                # Emit the signal with the StatsChart instance
                self.game_selected.emit(game_key, sport, status, stat_graph)
            else:
                print(f"No games found for {game_key}, {sport}")

    def spoiler_toggled(self, state):
        pushbuttons = self.findChildren(RadioGameButton)

        for button in pushbuttons:
            if button.time_label.text() in ("In Progress", "Half-time"):
                if state:
                    button.home_score_label.setText(button.property('home_score'))
                    button.away_score_label.setText(button.property('away_score'))
                else:

                    button.home_score_label.setText("--")
                    button.away_score_label.setText("--")

    def update_ui_scores(self, sport):
        print(f"Update UI task triggered current sport is {sport}")

        if sport is None:
            print("No sport specified")
            return

        sport_games = None
        if sport == ac.app_leagues[0]:
            sport_games = da.nba_scheduled_games

        elif sport == ac.app_leagues[1]:
            sport_games = da.nfl_scheduled_games

        elif sport == ac.app_leagues[2]:
            sport_games = da.nhl_scheduled_games

        if sport_games is None:
            print(f"No games found for {sport}")
            return

        game_buttons = self.findChildren(RadioGameButton)
        for button in game_buttons:
            # print(f"button: {button.property('game_key')}")
            game_id = None
            home_score = 0
            away_score = 0
            real_home_score = 0
            real_away_score = 0
            status = None

            for game_key, game in sport_games.items():
                game_id = game["game_id"]
                status = game.get("status")

                if game_id == button.property('game_key'):
                    # print(f"dataset: {game_id}")

                    if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                        box_score = da.get_box_score(game_id, sport)
                        if box_score:
                            real_home_score = box_score.get("home_score")
                            real_away_score = box_score.get("away_score")

                            if user_preferences.spoilers:
                                home_score = real_home_score
                                away_score = real_away_score
                            else:
                                home_score = "--"
                                away_score = "--"

                    else:
                        home_score = game.get("home_score")
                        away_score = game.get("away_score")
                        real_home_score = home_score
                        real_away_score = away_score

                    break

            button.home_score_label.setText(home_score)
            button.away_score_label.setText(away_score)
            button.setProperty("home_score", str(real_home_score))
            button.setProperty("away_score", str(real_away_score))
            button.time_label.setText(status)

            if button.isChecked():
                self.game_selected.emit(game_id, sport, status)

    def show_graph(self, button, sport):
        if button:
            home_team_id = button.property('home_team_id')
            away_team_id = button.property('away_team_id')
            home_team_name = button.home_label.text()
            away_team_name = button.away_label.text()

            df_home_team_stats = da.get_team_stats(home_team_id, sport)
            df_away_team_stats = da.get_team_stats(away_team_id, sport)

            if len(df_home_team_stats) > 0 and len(df_away_team_stats) > 0:
                self.stat_graph = StatsChart(home_team_name, away_team_name, df_home_team_stats, df_away_team_stats,
                                             sport)
                global graph
                graph = self.stat_graph
                # print(shared.current_game)
                #
                # self.stat_graph.show()
            else:
                print("No statistics data.")