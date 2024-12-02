from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from buttons.toggle_button import ToggleButton
from common.shared import user_preferences
from labels.image import Image


class SportsButton(ToggleButton):
    def __init__(self, key=None, text_label=None, action=None, logo=None):
        super().__init__(text=None, action=None)

        self.key = key
        self.action = action

        initial_state = user_preferences.sports_enabled.get(key, False)
        self.setChecked(initial_state)

        self.horizontal_layout = QHBoxLayout()
        self.logo = None
        self.text_label = None

        if self.action:
            self.toggled.connect(self.action)

        self.get_text(text_label)
        self.get_logo(logo)
        self.setFixedSize(250, 100)
        self.setLayout(self.horizontal_layout)

    def get_text(self, text_label):
        self.text_label = QLabel(text_label)
        self.text_label.setStyleSheet("""
                                      color: black;
                                      background-color: transparent;
                                      font-size: 45px;
                                      """)
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addSpacerItem(spacer)
        self.horizontal_layout.addWidget(self.text_label)

    def get_logo(self, logo):
        self.logo = Image(logo, 60, 60)
        self.logo.setStyleSheet("background-color: transparent;")
        spacer = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addSpacerItem(spacer)
        self.horizontal_layout.addWidget(self.logo)
