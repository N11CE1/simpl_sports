from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from labels.image import Image as Image


class ImageWithText(QWidget):
    def __init__(self, image, text):
        super().__init__()
        self.vertical_layout = QVBoxLayout()
        self.image = None
        self.text = None
        self.get_image(image)
        self.get_text(text)
        self.setLayout(self.vertical_layout)

    def get_image(self, image):
        self.image = Image(image)
        self.vertical_layout.addWidget(self.image)
        self.vertical_layout.setAlignment(Qt.AlignCenter)

    def get_text(self, text):
        self.text = QLabel(text)
        self.vertical_layout.addWidget(self.text)
        self.vertical_layout.setAlignment(Qt.AlignCenter)
