from PyQt5.QtWidgets import QPushButton
from shared import user_preferences


class StyledButton(QPushButton):
    def __init__(self, text, action=None, style_key=None):
        super().__init__(text)
        self.custom_action = action
        if style_key:
            self.setStyleSheet(CSS_STYLES[style_key])

    def execute_custom_action(self, checked):
        if self.custom_action:
            self.custom_action(checked)


class ToggleButton(StyledButton):
    STYLE_KEYS = {
        'true': 'TOGGLE_BUTTON_ON_STYLE',
        'false': 'TOGGLE_BUTTON_OFF_STYLE',
    }

    def __init__(self, text, action=None):
        super().__init__(text, action, self.STYLE_KEYS['false'])
        self.setCheckable(True)
        self.toggled.connect(self.update_style)

    def update_style(self, checked):
        style_key = self.STYLE_KEYS['true'] if checked else self.STYLE_KEYS['false']
        self.setStyleSheet(CSS_STYLES[style_key])


class SpoilersButton(ToggleButton):
    STYLE_KEYS = {
        'true': 'SPOILERS_BUTTON_ON_STYLE',
        'false': 'SPOILERS_BUTTON_OFF_STYLE',
    }

    def __init__(self, text, action=None):
        super().__init__(text, action)
        self.setFixedSize(230, 80)


class SportsButton(ToggleButton):
    def __init__(self, key, text, action):
        super().__init__(text, action)
        self.setChecked(user_preferences.sports_enabled[key])
        self.setFixedSize(350, 120)


class PushButton(StyledButton):
    STYLE_KEY = 'PUSH_BUTTON_STYLE'

    def __init__(self, text, action):
        super().__init__(text, action, self.STYLE_KEY)
        self.clicked.connect(action)
        self.setFixedSize(150, 80)


# Define styles in a separate module or at the top of this module for easier modification
CSS_STYLES = {
    'TOGGLE_BUTTON_OFF_STYLE': """
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 5px solid #D9D9D9;
            border-radius: 15px;
        """,
    'TOGGLE_BUTTON_ON_STYLE': """
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 5px solid #007AFF;
            border-radius: 15px;
        """,
    'SPOILERS_BUTTON_OFF_STYLE': """
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 5px solid #D9D9D9;
            border-radius: 15px;
        """,
    'SPOILERS_BUTTON_ON_STYLE': """
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 5px solid #D9D9D9;
            border-color: #007AFF;
            border-radius: 15px;
        """,
    'PUSH_BUTTON_STYLE': """
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 2px solid #D9D9D9;
            border-radius: 15px;
        """
}
