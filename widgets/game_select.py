from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QButtonGroup

from buttons.radio_game_button import RadioGameButton
from common import shared


class GameSelection(QWidget):
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
        self.setStyleSheet("background: transparent;")
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        scroll_area.setFixedHeight(195)
        scroll_area.setStyleSheet(self.SCROLL_AREA_STYLE)

        self.main_layout.addWidget(scroll_area)

        container = QWidget(self)
        self.hbox = QHBoxLayout()
        container.setLayout(self.hbox)

        scroll_area.setWidget(container)

        self.games_button_group = QButtonGroup()
        self.games_button_group.setExclusive(True)
        # self.update_games(sport=None)

    def update_games(self, sport):
        print(f"Game Selection updated for sport {sport}")
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
        for sport_dict in shared.test_games:
            if sport in sport_dict:
                sport_games = sport_dict[sport]
                break

        if sport_games is None:
            print(f"No games found for {sport}")
            return

        for games in sport_games.values():
            date = games.get("date", None)
            home = games.get("home", None)
            home_score = games.get("home_score", None)
            away = games.get("away", None)
            away_score = games.get("away_score", None)
            time = games.get("time", None)

            if time is not None:
                radio_button = RadioGameButton(date=date, home=home, home_score=home_score,
                                               away=away, away_score=away_score, time=time)
                self.games_button_group.addButton(radio_button)
                self.hbox.addWidget(radio_button)
