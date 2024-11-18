from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QButtonGroup,
                             QScrollArea, QSpacerItem)

import gui
import buttons
import gui_prefs
import labels
import shared


class MainMenu(QWidget):

    prefs_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.set_main_layout()

    def set_main_layout(self):
        self.clear_layout(self.main_layout)

        left_vbox = QVBoxLayout()
        top_hbox = QHBoxLayout()
        right_vbox = QVBoxLayout()

        logo = labels.Image("logo.png")
        prefs_button = buttons.push_button("Preferences", self.preferences_click)
        prefs_button.setFixedSize(200, 100)
        prefs_button.clicked.connect(self.emit_prefs_signal)
        sports_selection = SportSelection()
        game_selection = GameSelection()
        expanded_view = QSpacerItem(500, 500)
        left_vbox.addWidget(logo, alignment=Qt.AlignLeft)
        left_vbox.addWidget(sports_selection)
        top_hbox.addWidget(game_selection)
        top_hbox.addWidget(prefs_button)
        right_vbox.addLayout(top_hbox)
        right_vbox.addItem(expanded_view)
        self.main_layout.addLayout(left_vbox)
        self.main_layout.addLayout(right_vbox)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
            else:
                pass

    def preferences_click(self):
        pass

    def emit_prefs_signal(self):
        self.prefs_button_clicked.emit()


class SportSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(400)
        scroll_area.setMaximumHeight(500)
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
                width: 12px;
                margin: 0px 0px 0px 0px;
                padding: 0px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
            """)
        self.main_layout.addWidget(scroll_area)

        container = QWidget(self)
        self.vbox = QVBoxLayout()
        container.setLayout(self.vbox)

        scroll_area.setWidget(container)

        self.sports_button_group = QButtonGroup()
        self.sports_button_group.setExclusive(True)
        self.update_sports()

    def update_sports(self):
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget:
                self.sports_button_group.removeButton(widget)
                widget.deleteLater()

        for sports in shared.user_preferences.sports_order.values():
            radio_button = buttons.RadioSportsButton(sports.upper())
            self.sports_button_group.addButton(radio_button)
            self.vbox.addWidget(radio_button)


class GameSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(500)
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
                width: 12px;
                margin: 0px 0px 0px 0px;
                padding: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
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
                radio_button = buttons.RadioGameButton(date=date, home=home, home_score=home_score,
                                                       away=away, away_score=away_score, time=time)
                self.games_button_group.addButton(radio_button)
                self.hbox.addWidget(radio_button)

