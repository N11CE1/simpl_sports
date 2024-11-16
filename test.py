class RadioButton(QRadioButton):
    def __init__(self, text, parent=None, action=None, initial_state=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedSize(250, 80)

        self.custom_action = action
        if self.custom_action:
            self.toggled.connect(self.execute_custom_action)
        if initial_state is not None:
            self.setChecked(initial_state)

        self.setStyleSheet(self.unchecked_style())
        self.toggled.connect(self.update_style)

    @staticmethod
    def unchecked_style():
        return """
            QRadioButton{
                font: helvetica;
                font-size: 30px;
                colour: black;
                background-color: #F5F5F5;
                border: 5px solid #D9D9D9;
                border-radius: 15px;
                qproperty-alignment: "AlignCenter";
            }
            QRadioButton::indicator {
                width: 0px;
            }
        """

    @staticmethod
    def checked_style():
        return """
            QRadioButton{
                font: helvetica;
                font-size: 30px;
                colour: black;
                background-color: #F5F5F5;
                border: 5px solid #007AFF;
                border-radius: 15px;
                qproperty-alignment: "AlignCenter";
            }
            QRadioButton::indicator {
                width: 0px;
            }
        """

    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.checked_style())
        else:
            self.setStyleSheet(self.unchecked_style())

    def execute_custom_action(self, checked):
        if self.custom_action:
            self.custom_action(checked)