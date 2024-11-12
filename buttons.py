from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ToggleButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)  # Make the button checkable
        self.setStyleSheet(self.false_style())
        self.toggled.connect(self.update_style)

    def false_style(self):
        return """
        QPushButton{
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 60px;
            border: 2px solid #D9D9D9;
            border-radius: 15px;
        }
        """

    def true_style(self):
        return """
                QPushButton{
                    color: black;
                    background-color: lightblue;
                    font: helvetica;
                    font-size: 60px;
                    border: 2px solid #D9D9D9;
                    border-radius: 15px;
                }
                """

    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.true_style())
        else:
            self.setStyleSheet(self.false_style())


def sports_button(text):
    # Initialize the QLabel with the provided text
    label = ToggleButton(text)

    # Set dimensions
    label.setFixedSize(500, 200)

    return label
