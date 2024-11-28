from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class SmallText(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
                font-helvetica;
                font-size: 15px;
                color: black;
                """)