from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout

import buttons


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
        prefs_button = buttons.PushButton("Preferences", self.preferences_click)
        prefs_button.setFixedSize(200, 100)
        prefs_button.clicked.connect(self.emit_prefs_signal)
        self.main_layout.addWidget(prefs_button)

    def preferences_click(self):
        pass

    def emit_prefs_signal(self):
        self.prefs_button_clicked.emit()
