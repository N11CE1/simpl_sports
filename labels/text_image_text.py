from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from labels.image import Image as Image


class TextImageText(QWidget):
    def __init__(self, text1, image, text2):
        super().__init__()
        self.vertical_layout = QVBoxLayout()
        self.text1 = None
        self.image = None
        self.text2 = None
        self.get_text1(text1)
        self.get_image(image)
        self.get_text2(text2)
        self.setLayout(self.vertical_layout)

    def get_text1(self, text1):
        self.text1 = QLabel(text1)
        self.vertical_layout.addWidget(self.text1)
        self.vertical_layout.setAlignment(Qt.AlignCenter)

    def get_image(self, image):
        self.image = Image(image)
        self.vertical_layout.addWidget(self.image)
        self.vertical_layout.setAlignment(Qt.AlignCenter)

    def get_text2(self, text2):
        self.text2 = QLabel(text2)
        self.vertical_layout.addWidget(self.text2)
        self.vertical_layout.setAlignment(Qt.AlignCenter)