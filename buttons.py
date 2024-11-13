from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ToggleButton(QPushButton):
    def __init__(self, text, action=None):
        super().__init__(text)
        self.setCheckable(True)  # making button check-able aka stateful
        self.setStyleSheet(self.false_style())
        self.toggled.connect(self.update_style)
        self.toggled.connect(self.execute_custom_action)
        self.custom_action = action

    def false_style(self):
        return """
        QPushButton{
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 50px;
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
                    font-size: 50px;
                    border: 2px solid #D9D9D9;
                    border-radius: 15px;
                }
                """

    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.true_style())
        else:
            self.setStyleSheet(self.false_style())

    def execute_custom_action(self, checked):
        if self.custom_action:
            self.custom_action(checked)


def sports_button(text, action=None):
    s_button = ToggleButton(text, action=action)
    s_button.setFixedSize(400, 150)
    return s_button

def push_button(text, action=None):
    p_button = QPushButton(text)
    p_button.clicked.connect(action)
    p_button.setFixedSize(200, 100)
    p_button.setStyleSheet("""
        color: black;
        background-color: #F5F5F5;
        font: helvetica;
        font-size: 30px;
        border: 2px solid #D9D9D9;
        border-radius: 15px;
        """)
    return p_button
