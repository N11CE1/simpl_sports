from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
from labels.image import Image as Image
from buttons.toggle_button import ToggleButton


class RadioSportsButton(ToggleButton):
    def __init__(self, text_label=None, action=None, logo=None):
        super().__init__(text=None, action=None)
        self.horizontal_layout = QHBoxLayout()
        self.logo = None
        self.text_label = None
        self.action = action
        self.get_text(text_label)
        self.get_logo(logo)
        self.setChecked(False)
        self.setFixedSize(250, 100)
        self.setLayout(self.horizontal_layout)

    def get_text(self, text_label):
        self.text_label = QLabel(text_label)
        self.text_label.setStyleSheet("font-size: 45px;")
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addSpacerItem(spacer)
        self.horizontal_layout.addWidget(self.text_label)

    def get_logo(self, logo):
        self.logo = Image(logo, 60, 60)
        spacer = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout.addSpacerItem(spacer)
        self.horizontal_layout.addWidget(self.logo)
