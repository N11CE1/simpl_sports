from buttons.toggle_button import ToggleButton
from common.shared import user_preferences


class SportsButton(ToggleButton):
    def __init__(self, key, text, action):
        super().__init__(text, action)
        self.setChecked(user_preferences.sports_enabled[key])
        self.setFixedSize(350, 120)