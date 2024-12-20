import collections.abc

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QFrame, QSizePolicy

from graph.graph_team_record_analysis import StatsChart
from labels.image import Image as Image
from labels.small_text import SmallText as SmallText
from labels.text_image_text import TextImageText as TextImageText
from widgets.main_sport_select import SportSelection as MainSportSelection
from common.shared import nba as nba, nfl as nfl, nhl as nhl, user_preferences
from common.shared import current_game as current_game
from labels.stats_label import StatsLabel as StatsLabel
from graph.graph_team_record_analysis import StatsChart

from api import data_operations as do
from api import api_constants as ac
from api import datasets as da


class GameExpandedView(QWidget):
    SCROLL_AREA_STYLE = """  
            QScrollArea {
            border: 2px solid #ccc;
            border-radius: 10px;
            background: transparent;
            padding-right: 0px;
            }
            
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            
            QScrollBar:horizontal {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            QScrollBar:vertical {
                width: 10px;
                background: transparent;
                border-radius: 4px;
                margin-top: 5px;
                margin-bottom: 5px;
                margin-right: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: #888;
                min-width: 6px;
                border-radius: 3px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
            QScrollBar::left-arrow:vertical, QScrollBar::right-arrow:vertical {
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
        self.setStyleSheet("background: transparent;")
        self.sport = nba
        self.game_key = 0
        self.home = None
        self.home_score = None
        self.away = None
        self.away_score = None
        self.stats_chart = None
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        scroll_area = self._create_styled_scroll_area()
        self.main_layout.addWidget(scroll_area)
        container = QWidget(self)
        self.score_and_stats = QVBoxLayout()
        self.score_view = QHBoxLayout()
        self.stats = QGridLayout()
        self.score_and_stats.addLayout(self.score_view)
        self.score_and_stats.addLayout(self.stats)
        container.setLayout(self.score_and_stats)
        scroll_area.setWidget(container)

    def _create_styled_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        scroll_area.setFixedHeight(450)
        self._style_scroll_area(scroll_area)
        return scroll_area

    def _style_scroll_area(self, scroll_area):
        scroll_area.setStyleSheet(self.SCROLL_AREA_STYLE)

    def update_game(self, game_key, sport_name, status, stat_graph):
        print(f"game_key = {game_key}, sport = {sport_name}")

        if self.stats_chart:
            self.score_and_stats.removeWidget(self.stats_chart)
            self.stats_chart.deleteLater()
            self.stats_chart = None

        ## Original Code
        sport_map = {"nba": nba, "nfl": nfl, "nhl": nhl}
        sport = sport_map.get(sport_name.lower())
        if sport is None:
            print(f"Sport {sport_name} is unknown")

        while self.score_view.count():
            item = self.score_view.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        while self.stats.count():
            item = self.stats.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if sport_name in (ac.app_leagues[0], ac.app_leagues[1], ac.app_leagues[2]):

            if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                # game_box_score = adm.game_box_score(game_key, sport_name)
                game_box_score = da.get_box_score(game_key, sport_name)
            else:
                game_box_score = da.get_static_games(game_key, sport_name)

            # game_box_score = da.get_static_games(game_key, sport_name)

            # if status in ("In Progress", "Half-time", "Closed"):
            #     game_box_score = da.get_box_score(game_key, sport_name)
            # else:
            #     game_box_score = da.get_static_games(game_key, sport_name)


            # if status.lower() in ("In Progress".lower(), "Half-time".lower()):
            #     box_score = da.get_box_score(game_key, sport)
            #     home_score = box_score.get("home_score")
            #     away_score = box_score.get("away_score")
            # else:
            #     home_score = game.get("home_score")
            #     away_score = game.get("away_score"

            if game_box_score is None:
                print(f"No game found for key {game_key}")
                return
            else:
                if sport_name == ac.app_leagues[0]:
                    df_home_team_info = do.get_team_info(short_name=game_box_score.get('home'), sportsdb_id=sport_name)
                    df_away_team_info = do.get_team_info(short_name=game_box_score.get('away'), sportsdb_id=sport_name)
                    home_image = do.get_team_image(short_name=game_box_score.get('home'), sportsdb_id=sport_name)
                    away_image = do.get_team_image(short_name=game_box_score.get('away'), sportsdb_id=sport_name)
                else:
                    df_home_team_info = do.get_team_info(name=game_box_score.get('home_name'), sportsdb_id=sport_name)
                    df_away_team_info = do.get_team_info(name=game_box_score.get('away_name'), sportsdb_id=sport_name)
                    home_image = do.get_team_image(name=game_box_score.get('home_name'), sportsdb_id=sport_name)
                    away_image = do.get_team_image(name=game_box_score.get('away_name'), sportsdb_id=sport_name)

                self.status = game_box_score.get('status')

                score_home = game_box_score.get('home_score')
                score_away = game_box_score.get('away_score')
                show_leader_boards = True

                if user_preferences.spoilers == False:
                    if status.lower() in ("In Progress".lower(), "Half-time".lower()):
                        score_home = "--"
                        score_away = "--"
                        show_leader_boards = False


                self.home = df_home_team_info.loc[0, 'name'] if not df_home_team_info.empty else game_box_score.get('home_name')
                self.home_score = score_home
                self.away = df_away_team_info.loc[0, 'name'] if not df_away_team_info.empty else game_box_score.get('away_name')
                self.away_score = score_away
                # print(self.home, self.home_score, self.away, self.away_score)

                self.home_team = TextImageText(str(self.home), home_image, str(self.home_score))
                self.home_team.setProperty("location", "home")
                self.home_team.setProperty("home_score", str(game_box_score.get('home_score')))
                self.vs = Image("images/vs image.png")
                self.away_team = TextImageText(str(self.away), away_image, str(self.away_score))
                self.away_team.setProperty("location", "away")
                self.away_team.setProperty("away_score", str(game_box_score.get('away_score')))
                self.score_view.addWidget(self.home_team)
                self.score_view.addWidget(self.vs)
                self.score_view.addWidget(self.away_team)

                # if show_leader_boards:

                if sport_name in (ac.app_leagues[0], ac.app_leagues[2]):
                    params = {}

                    if sport_name == ac.app_leagues[0]:
                        params_header = f"{'Name'.ljust(25)}{'Pts'.ljust(5)}{'Rbs'.ljust(5)}{'Ast'.ljust(5)}"
                    elif sport_name == ac.app_leagues[2]:
                        params_header = f"{'Name'.ljust(25)}{'Pts'.ljust(5)}{'Gls'.ljust(5)}{'Ast'.ljust(5)}"

                    params["header"] = params_header
                    a = 0
                    if game_box_score["home_leader_boards"] is not None:
                        for key, player in game_box_score["home_leader_boards"].items():
                            params[f'param{a}'] = f"{player["name"].ljust(25)}{player["points"].ljust(5)}{player["rebounds"].ljust(5)}{player["assists"].ljust(5)}"
                            a += 1

                        self.stat1 = StatsLabel(title="Home Team Leaderboards", **params)
                        self.stats.addWidget(self.stat1, 0, 0)

                    params = {}
                    params["Header"] = params_header
                    a = 0
                    if game_box_score["away_leader_boards"] is not None:
                        for key, player in game_box_score["away_leader_boards"].items():
                            params[f'param{a}'] = f"{player["name"].ljust(25)}{player["points"].ljust(5)}{player["rebounds"].ljust(5)}{player["assists"].ljust(5)}"
                            a += 1

                        self.stat2 = StatsLabel(title="Away Team Leaderboards", **params)
                        self.stats.addWidget(self.stat2, 0, 1)

                if show_leader_boards == False:
                    self.spoiler_toggled(False)

        if stat_graph:
            self.stats_chart = stat_graph
            self.stats_chart.setParent(self)  # Set the parent to this widget
            self.stats_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.stats_chart.setMinimumSize(400, 600)
            self.score_and_stats.addWidget(self.stats_chart)
        else:
            print("No statistics data available.")

        self.spoiler_toggled(user_preferences.spoilers)

    def spoiler_toggled(self, state):
        print("spoiler_toggled method called in GameExpandedView")
        # Find all QPushButton widgets in the form
        textImagetext = self.findChildren(TextImageText)

        for textImagetext in textImagetext:
            if self.status in ("In Progress", "Half-time"):
                if state:
                    if textImagetext.property("location") == "home":
                        textImagetext.text2.setText(textImagetext.property("home_score"))
                    else:
                        textImagetext.text2.setText(textImagetext.property("away_score"))
                else:
                    textImagetext.text2.setText("--")
                    textImagetext.text2.setText("--")

        frames = self.findChildren(QFrame)  # Find all QFrame widgets
        for frame in frames:
            if frame.objectName() == 'StatsLabel':
                if user_preferences.spoilers:
                    frame.show()
                else:
                    frame.hide()
