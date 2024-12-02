from PyQt5.QtGui import QIcon
from buttons.picture_button import PictureButton as PictureButton
from common.shared import user_preferences as user_preferences
from PyQt5.QtCore import pyqtSignal


class SpoilerToggle(PictureButton):
    spoiler_toggled = pyqtSignal(bool)
    def __init__(self, display_image=None, secondary_image=None, x=None, y=None, click_function=None):
        super().__init__(display_image, x, y, click_function)
        self.display_image = None
        self.initial_state()
        self.secondary_image = secondary_image
        self.setIcon(QIcon(self.display_image))
        self.clicked.connect(self.toggle_image)

    def initial_state(self):
        if user_preferences.spoilers:
            self.display_image = "images/spoilers_on.png"
        else:
            self.display_image = "images/spoilers_off.png"
        self.setIcon(QIcon(self.display_image))

    def toggle_image(self):
        if user_preferences.spoilers:
            user_preferences.spoilers = False
            print("spoilers off")
        elif not user_preferences.spoilers:
            user_preferences.spoilers = True
            print("spoilers on")
        self.initial_state()
        self.spoiler_toggled.emit(user_preferences.spoilers)

