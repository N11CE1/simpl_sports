from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea
from labels.image_with_text import ImageWithText as ImageWithText
from labels.image import Image as Image
from labels.small_text import SmallText as SmallText
from labels.text_image_text import TextImageText as TextImageText
from widgets.main_sport_select import SportSelection as MainSportSelection
from common.shared import epl_expanded_games as epl_expanded_games


# class GameExpandedView(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.container = None
#         self.score_layout = None
#         self.statistics_layout = None
#         self.team1 = None
#         self.vs = None
#         self.team2 = None
#         self.stat1 = None
#         self.stat2 = None
#         self.stat3 = None
#         self.stat4 = None
#         self.setFixedSize(800, 500)
#         self.setStyleSheet("border: 1px solid black;")
#         self.init_ui()
#
#     def init_ui(self):
#
#         self.team1 = ImageWithText("images/logo.png", "Team 1")
#         self.vs = Image("images/logo.png")
#         self.team2 = ImageWithText("images/logo.png", "Team 2")
#
#         self.score_layout = QHBoxLayout()
#         self.score_layout.addWidget(self.team1)
#         self.score_layout.addWidget(self.vs)
#         self.score_layout.addWidget(self.team2)
#
#         self.stat1 = SmallText("State 1 Here")
#         self.stat2 = SmallText("State 2 Here")
#         self.stat3 = SmallText("State 3 Here")
#         self.stat4 = SmallText("State 4 Here")
#
#         self.statistics_layout = QGridLayout()
#         self.statistics_layout.addWidget(self.stat1, 0, 0)
#         self.statistics_layout.addWidget(self.stat2, 0, 1)
#         self.statistics_layout.addWidget(self.stat3, 1, 0)
#         self.statistics_layout.addWidget(self.stat4, 1, 1)
#
#         self.container = QVBoxLayout()
#         self.container.addLayout(self.score_layout)
#         self.container.addLayout(self.statistics_layout)
#         self.setLayout(self.container)

class GameExpandedView(QWidget):
    game_selected = pyqtSignal(int)
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
        self.sport = epl_expanded_games
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

        self.update_game(self.game_key, self.sport)

        self.home_team = TextImageText(self.home, "images/logo.png", self.home_score)
        self.vs = Image("images/logo.png")
        self.away_team = TextImageText(self.away, "images/logo.png", self.away_score)
        self.score_view.addWidget(self.home_team)
        self.score_view.addWidget(self.vs)
        self.score_view.addWidget(self.away_team)

        self.stat1 = SmallText("Stat 1")
        self.stat2 = SmallText("Stat 2")
        self.stat3 = SmallText("Stat 3")
        self.stat4 = SmallText("Stat 4")

        self.stats.addWidget(self.stat1, 0, 0)
        self.stats.addWidget(self.stat2, 0, 1)
        self.stats.addWidget(self.stat3, 1, 0)
        self.stats.addWidget(self.stat4, 1, 1)

    def _create_styled_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        scroll_area.setFixedHeight(400)
        self._style_scroll_area(scroll_area)
        return scroll_area

    def _style_scroll_area(self, scroll_area):
        scroll_area.setStyleSheet(self.SCROLL_AREA_STYLE)

    def update_game(self, game_key, sport):
        while self.score_view.count():
            item = self.score_view.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if game_key in sport:
            game = sport[game_key]
            self.home = game.get('home')
            self.home_score = game.get('home_score')
            self.away = game.get('away')
            self.away_score = game.get('away_score')
            print(self.home, self.home_score, self.away, self.away_score)
        else:
            print(f"No game found for key {game_key}")
