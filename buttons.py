from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QRadioButton, QWidget, \
    QVBoxLayout, QHBoxLayout, QLabel, QGridLayout  # importing QPushButton to be the basis of our buttons
from PyQt5.QtCore import Qt, QSize

from shared import user_preferences


# defining toggle button (has on/off state)
class ToggleButton(QPushButton):  # taking QPushButton as an argument because I'm just altering the existing button type
    def __init__(self, text=None, action=None):
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
                    border: 2px solid #D9D9D9;
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
                    border: 2px solid #D9D9D9;
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


class SpoilersButton(ToggleButton):
    def __init__(self, text, action=None, initial_state=None):
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
        

# defining sports button as a type of toggle button which takes 2 arguments
# (the text it will display and the action it takes)
def sports_button(key, text, action):
    s_button = ToggleButton(text, action)
    s_button.setChecked(user_preferences.sports_enabled[key])  # setting checked state with data in user_preferences
    s_button.setFixedSize(350, 120)  # defining the size of the sports button
    return s_button  # returns the s_button object to the caller


class RadioSportsButton(ToggleButton):
    def __init__(self, text=None, action=None):
        super().__init__(text, action)
        self.text = text
        self.action = action
        self.setChecked(False)
        self.setFixedSize(250, 100)  # defining the size of the sports button


class RadioGameButton(ToggleButton):
    def __init__(self, date=None, home=None, home_score=None, away=None, away_score=None, time=None, action=None):
        super().__init__(action)
        self.set_font(self)
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
            items.setStyleSheet(self.set_font(self))

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
    def set_font(self):
        return """
        font: helvetica;
        font-size: 20px;
        color: black;
        background-color: transparent;
        """


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


# # class PictureButton(ToggleButton):
# #     def __init__(self, display_image=None, x=None, y=None, action=None):
# #         super().__init__()
# #         if display_image:
# #             self.setPixmap(QPixmap(display_image))
# #         if x is not None and y is not None:
# #             self.setFixedSize(x, y)
# #         self.main_layout = QHBoxLayout()
# #         self.main_layout.setContentsMargins(0, 0, 0, 0)
# #
# #         self.image = QLabel()
# #
# #         self.set_image(display_image, x, y)
# #
# #         if action is not None:
# #             self.clicked.connect(action)
# #
# #         self.main_layout.addWidget(self.image)
# #         self.setLayout(self.main_layout)
# #
# #         self.setStyleSheet("""
# #                             color: transparent;
# #                             background-color: transparent;
# #                             border: 0px solid #D9D9D9;
# #                             """)
#
#     def set_image(self, image_path, x, y):
#         pixmap = QPixmap(image_path)
#         scaled_pixmap = pixmap.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#
#         self.image.setPixmap(scaled_pixmap)
#
#         self.image.setScaledContents(True)
#         self.image.setFixedSize(scaled_pixmap.size())

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
