from PyQt5.QtWidgets import QPushButton, QRadioButton, QWidget, \
    QVBoxLayout, QHBoxLayout, QLabel  # importing QPushButton to be the basis of our buttons
from PyQt5.QtCore import Qt
from shared import user_preferences


# defining toggle button (has on/off state)
class ToggleButton(QPushButton):  # taking QPushButton as an argument because I'm just altering the existing button type
    def __init__(self, text, action=None):
        super().__init__(text)
        self.setCheckable(True)  # making button check-able aka stateful
        self.setStyleSheet(self.false_style())  # set false style as default style
        self.toggled.connect(self.update_style)  # connects update style method to button presses
        self.toggled.connect(self.execute_custom_action)  # connects custom action to button presses
        self.custom_action = action  # custom action == action defined in __init__ which is None by default

    # defining visual style of toggle button in off state to be returned
    # to the update style method
    def false_style(self):
        # self.SetStyleSheet takes CSS like code as string, making it an easy way to set visual style of widget
        return """
                QPushButton{
                    color: black;
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 50px;
                    border: 5px solid #D9D9D9;
                    border-radius: 15px;
                }
                """

    # defining visual style of toggle button in on state to be returned
    # to the update style method
    def true_style(self):
        return """
                QPushButton{
                    color: black;
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 50px;
                    border: 5px solid #D9D9D9;
                    border-color: #007AFF;
                    border-radius: 15px;
                }
                """

    # method to set style off button based on its state
    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.true_style())
        else:
            self.setStyleSheet(self.false_style())

    # executes a custom action based on the state of the button (checked = on)
    def execute_custom_action(self, checked):
        if self.custom_action:  # checks for existence of self.custom_action
            self.custom_action(checked)  # if self.custom_action exists, execute the custom action if button is checked

class RadioButton(QRadioButton):
    def __init__(self, parent=None, action=None, initial_state=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(230, 80)

        if initial_state is not None:
            self.setChecked(initial_state)

        self.update_style(self.isChecked())

        self.toggled.connect(self.update_style)

        self.custom_action = action
        if self.custom_action:
            self.toggled.connect(self.execute_custom_action)

    def update_style(self, checked):
        if checked:
            self.setStyleSheet(self.checked_style())
        else:
            self.setStyleSheet(self.unchecked_style())

    def execute_custom_action(self, checked):
        if self.custom_action:
            self.custom_action(checked)

    @staticmethod
    def unchecked_style():
        return """
            QRadioButton{
                font: Helvetica;
                font-size: 30px;
                color: black;
                background-color: #F5F5F5;
                border: 3px solid #D9D9D9;
                border-radius: 15px;
                padding: 10px;
            }
            QRadioButton::indicator {
                color: #007AFF;
                width: 0px;
            }
        """

    @staticmethod
    def checked_style():
        return """
            QRadioButton{
                font: Helvetica;
                font-size: 30px;
                color: black;
                background-color: #F5F5F5;
                border: 3px solid #007AFF;
                border-radius: 15px;
                padding: 10px;
            }
            QRadioButton::indicator {
                color: #007AFF;
                background-color: #007AFF;
                width: 0px;
            }
        """


# defining sports button as a type of toggle button which takes 2 arguments
# (the text it will display and the action it takes)
def sports_button(key, text, action):
    s_button = ToggleButton(text, action)
    s_button.setChecked(user_preferences.sports_enabled[key])  # setting checked state with data in user_preferences
    s_button.setFixedSize(400, 150)  # defining the size of the sports button
    return s_button  # returns the s_button object to the caller


# defining standard push button
# push_button is not a class because the QPushButton class already does everything we need it to
# we're just defining an object of the QPushButton class and customising its look for reusability
def push_button(text, action):  # takes text and action arguments
    p_button = QPushButton(text)
    p_button.clicked.connect(action)  # performs action on click
    p_button.setFixedSize(150, 80)  # setting dimensions
    p_button.setStyleSheet("""
        color: black;
        background-color: #F5F5F5;
        font: helvetica;
        font-size: 30px;
        border: 2px solid #D9D9D9;
        border-radius: 15px;
        """)  # looks stuff all set in style sheet
    return p_button  # returns p_button object to caller
