import collections.abc

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
from labels.image import Image as Image
from labels.small_text import SmallText as SmallText
from labels.text_image_text import TextImageText as TextImageText
from widgets.main_sport_select import SportSelection as MainSportSelection
from common.shared import nba as nba, nfl as nfl, nhl as nhl, epl as epl
from labels.stats_label import StatsLabel as StatsLabel
from api import api_data_manager as adm
from api import data_operations as do
from api import api_constants as ac

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
        self.sport = epl
        self.game_key = 0
        self.home = None
        self.home_score = None
        self.away = None
        self.away_score = None
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

    def update_game(self, game_key, sport_name):
        print(f"game_key = {game_key}, sport = {sport_name}")

        ## Original Code
        sport_map = {"nba": nba, "nfl": nfl, "nhl": nhl, "epl": epl}
        sport = sport_map.get(sport_name.lower())
        if sport is None:
            print(f"Sport {sport_name} is unknown")

        # while self.score_view.count():
        #     item = self.score_view.takeAt(0)
        #     widget = item.widget()
        #     if widget:
        #         widget.deleteLater()
        # while self.stats.count():
        #     item = self.stats.takeAt(0)
        #     widget = item.widget()
        #     if widget:
        #         widget.deleteLater()

        # if isinstance(sport, collections.abc.Mapping) and game_key in sport:
        #     game = sport[game_key]
        #     self.home = game.get('home')
        #     self.home_score = game.get('home_score')
        #     self.away = game.get('away')
        #     self.away_score = game.get('away_score')
        #     print(self.home, self.home_score, self.away, self.away_score)
        # else:
        #     print(f"No game found for key {game_key}")
        #     return

        # self.home_team = TextImageText(self.home, "images/logo.png", self.home_score)
        # self.vs = Image("images/logo.png")
        # self.away_team = TextImageText(self.away, "images/logo.png", self.away_score)
        # self.score_view.addWidget(self.home_team)
        # self.score_view.addWidget(self.vs)
        # self.score_view.addWidget(self.away_team)

        # self.stat1 = StatsLabel(title="Stat 1", line1="line1", line2="line2")
        # self.stat2 = StatsLabel(title="Stat 2", line1="line1", line2="line2", line3="line3")
        # self.stat3 = StatsLabel(title="Stat 3", line1="line1", line2="line2", line3="line3", line4="line4")
        # self.stat4 = StatsLabel(titles="Stat 4", line1="line1", line2="line2", line3="line3",
        #                         line4="line4", line5="line5")
        #
        # self.stats.addWidget(self.stat1, 0, 0)
        # self.stats.addWidget(self.stat2, 0, 1)
        # self.stats.addWidget(self.stat3, 1, 0)
        # self.stats.addWidget(self.stat4, 1, 1)

        ## End of Original Code

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

            game_box_score = adm.game_box_score(game_key, sport_name)

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
                    df_home_team_info = do.get_team_info(name=game_box_score.get('home'), sportsdb_id=sport_name)
                    df_away_team_info = do.get_team_info(name=game_box_score.get('away'), sportsdb_id=sport_name)
                    home_image = do.get_team_image(name=game_box_score.get('home'), sportsdb_id=sport_name)
                    away_image = do.get_team_image(name=game_box_score.get('away'), sportsdb_id=sport_name)

                self.home = df_home_team_info.loc[0, 'name'] if not df_home_team_info.empty else game_box_score.get('home')
                self.home_score = game_box_score.get('home_score')
                self.away = df_away_team_info.loc[0, 'name'] if not df_away_team_info.empty else game_box_score.get('away')
                self.away_score = game_box_score.get('away_score')
                print(self.home, self.home_score, self.away, self.away_score)

                self.home_team = TextImageText(str(self.home), home_image, str(self.home_score))
                self.vs = Image("images/vs image.png")
                self.away_team = TextImageText(str(self.away), away_image, str(self.away_score))
                self.score_view.addWidget(self.home_team)
                self.score_view.addWidget(self.vs)
                self.score_view.addWidget(self.away_team)

                if sport_name in (ac.app_leagues[0], ac.app_leagues[2]):
                    params = {}

                    if sport_name == ac.app_leagues[0]:
                        params_header = f"{'Name'.ljust(25)}{'Pts'.ljust(5)}{'Rbs'.ljust(5)}{'Ast'.ljust(5)}"
                    elif sport_name == ac.app_leagues[2]:
                        params_header = f"{'Name'.ljust(25)}{'Pts'.ljust(5)}{'Gls'.ljust(5)}{'Ast'.ljust(5)}"

                    params["header"] = params_header
                    a = 0
                    for key, player in game_box_score["home_leader_boards"].items():
                        params[f'param{a}'] = f"{player["name"].ljust(25)}{player["points"].ljust(5)}{player["rebounds"].ljust(5)}{player["assists"].ljust(5)}"
                        a += 1

                    self.stat1 = StatsLabel(title="Home Team Leaderboards", **params)
                    self.stats.addWidget(self.stat1, 0, 0)

                    params = {}
                    params["Header"] = params_header
                    a = 0
                    for key, player in game_box_score["away_leader_boards"].items():
                        params[f'param{a}'] = f"{player["name"].ljust(25)}{player["points"].ljust(5)}{player["rebounds"].ljust(5)}{player["assists"].ljust(5)}"
                        a += 1

                    self.stat2 = StatsLabel(title="Away Team Leaderboards", **params)
                    self.stats.addWidget(self.stat2, 0, 1)
