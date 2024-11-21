from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import QSize

from shared import user_preferences


class ToggleButton(QPushButton):
    def __init__(self, text=None, action=None):
        super().__init__(text)
        self.setCheckable(True)  # making button check-able aka stateful
        self.setStyleSheet(self.false_style())  # set false style as default style
        self.toggled.connect(self.update_style)  # connects update style method to button presses
        self.toggled.connect(self.execute_custom_action)  # connects custom action to button presses
        self.custom_action = action  # custom action == action defined in __init__ which is None by default

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
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 50px;
                    border: 2px solid #D9D9D9;
                    border-color: #007AFF;
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


class SpoilersButton(ToggleButton):
    def __init__(self, text, action=None):
        super().__init__(text)
        self.setFixedSize(230, 80)
        self.custom_action = action

    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.true_style())
        else:
            self.setStyleSheet(self.false_style())

    def true_style(self):
        return """
            QPushButton{
                    color: black;
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 30px;
                    border: 2px solid #007AFF;
                    border-radius: 15px;
                }
                """

    def false_style(self):
        return """
            QPushButton{
                    color: black;
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 30px;
                    border: 2px solid #D9D9D9;
                    border-radius: 15px;
                }
                """

    def execute_custom_action(self, checked):
        if self.custom_action:
            self.custom_action(checked)
        

def sports_button(key, text, action):
    s_button = ToggleButton(text, action)
    s_button.setChecked(user_preferences.sports_enabled[key])
    s_button.setFixedSize(350, 120)
    return s_button


class RadioSportsButton(ToggleButton):
    def __init__(self, text=None, action=None):
        super().__init__(text, action)
        self.text = text
        self.action = action
        self.setChecked(False)
        self.setFixedSize(250, 100)


class RadioGameButton(ToggleButton):
    def __init__(self, date=None, home=None, home_score=None, away=None, away_score=None, time=None, action=None):
        super().__init__(action)
        self.set_font()
        self.layout = QVBoxLayout()
        self.score = QGridLayout()

        self.date_label = QLabel(date)
        self.home_label = QLabel(home)
        self.home_score_label = QLabel(home_score)
        self.away_label = QLabel(away)
        self.away_score_label = QLabel(away_score)
        self.time_label = QLabel(time)
        for items in [self.date_label, self.home_label, self.home_score_label,
                      self.away_label, self.away_score_label, self.time_label]:
            items.setStyleSheet(self.set_font())

        self.score.addWidget(self.home_label, 0, 0)
        self.score.addWidget(self.home_score_label, 0, 1)
        self.score.addWidget(self.away_label, 1, 0)
        self.score.addWidget(self.away_score_label, 1, 1)

        self.layout.addWidget(self.date_label)
        self.layout.addLayout(self.score)
        self.layout.addWidget(self.time_label)

        self.setLayout(self.layout)

        self.action = action
        self.setChecked(False)
        self.setFixedSize(150, 150)

    @staticmethod
    def set_font():
        return """
        font: helvetica;
        font-size: 20px;
        color: black;
        background-color: transparent;
        """


def push_button(text, action):
    p_button = QPushButton(text)
    p_button.clicked.connect(action)
    p_button.setFixedSize(150, 80)
    p_button.setStyleSheet("""
        color: black;
        background-color: #F5F5F5;
        font: helvetica;
        font-size: 30px;
        border: 2px solid #D9D9D9;
        border-radius: 15px;
        """)
    return p_button


class PictureButton(QPushButton):
    def __init__(self, display_image=None, x=None, y=None, click_function=None):
        super().__init__()
        if display_image:
            self.setIcon(QIcon(QPixmap(display_image)))
        if x is not None and y is not None:
            self.setIconSize(QSize(x, y))
        if click_function:
            self.clicked.connect(click_function)
        self.setStyleSheet("""
            border: 0px solid black;
            """)


class SpoilerToggle(PictureButton):
    def __init__(self, display_image=None, secondary_image=None, x=None, y=None, click_function=None):
        super().__init__(display_image, x, y, click_function)
        self.display_image = None
        self.initial_state()
        self.secondary_image = secondary_image
        self.setIcon(QIcon(self.display_image))
        self.clicked.connect(self.toggle_image)

    def initial_state(self):
        if user_preferences.spoilers:
            self.display_image = "spoilers_on.png"
        else:
            self.display_image = "spoilers_off.png"
        self.setIcon(QIcon(self.display_image))

    def toggle_image(self):
        if user_preferences.spoilers:
            user_preferences.spoilers = False
            print("spoilers off")
        elif not user_preferences.spoilers:
            user_preferences.spoilers = True
            print("spoilers on")
        self.initial_state()
