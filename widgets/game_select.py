from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QButtonGroup

from buttons.radio_game_button import RadioGameButton
from common import shared


class GameSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        scroll_area.setMaximumHeight(200)
        scroll_area.setStyleSheet("""
        QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                padding: 0px;
            }
            QScrollBar:horizontal {
                height: 6px;
                background: transparent;
                border-radius: 10px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-height: 6px;
                border-radius: 3px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QScrollBar::handle:horizontal:hover {
                background: #666;
            }
        """)
        self.main_layout.addWidget(scroll_area)

        container = QWidget(self)
        self.hbox = QHBoxLayout()
        container.setLayout(self.hbox)

        scroll_area.setWidget(container)

        self.games_button_group = QButtonGroup()
        self.games_button_group.setExclusive(True)
        self.update_games()

    def update_games(self):
        while self.hbox.count():
            item = self.hbox.takeAt(0)
            widget = item.widget()
            if widget:
                self.games_button_group.removeButton(widget)
                widget.deleteLater()

        for games in shared.test_games.values():
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
