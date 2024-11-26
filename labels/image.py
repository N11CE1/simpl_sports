from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class Image(QWidget):
    def __init__(self, display_image, width=200, height=200):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        display_image = display_image

        image = QLabel()

        pixmap = QPixmap(display_image)
        scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        image.setPixmap(scaled_pixmap)

        image.setScaledContents(True)
        image.setFixedSize(scaled_pixmap.size())

        self.main_layout.addWidget(image)

