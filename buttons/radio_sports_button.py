from buttons.toggle_button import ToggleButton


class RadioSportsButton(ToggleButton):
    def __init__(self, text=None, action=None):
        super().__init__(text, action)
        self.text = text
        self.action = action
        self.setChecked(False)
        self.setFixedSize(250, 100)