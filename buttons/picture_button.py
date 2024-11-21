from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


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