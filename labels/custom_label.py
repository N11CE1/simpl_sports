from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class CustomLabel(QLabel):
    def __init__(self, text, font_size=40, color='black'):
        super().__init__(text)
        self.color = color
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
                    font-family: 'Helvetica', sans-serif;
                    font-size: {font_size}px;
                    color: {color};
                    """)