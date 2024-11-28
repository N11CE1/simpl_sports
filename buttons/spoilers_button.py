from buttons.toggle_button import ToggleButton


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