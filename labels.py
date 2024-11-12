from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


def large_text_label(text):
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("""
                font-helvetica;
                font-size: 40px;
                color: black;
                """)
    return label
