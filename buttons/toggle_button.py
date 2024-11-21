from PyQt5.QtWidgets import QPushButton


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