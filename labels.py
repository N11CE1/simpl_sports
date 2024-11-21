from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout  # importing QLabel to be the basis of our labels
from PyQt5.QtCore import Qt  # importing Qt for alignment abilities
from PyQt5.QtGui import QPixmap


class CustomLabel(QLabel):
    def __init__(self, text, font_size=40, color='black'):
        super().__init__(text)
        self.color = color
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
                    font-family: 'Helvetica', sans-serif;
                    font-size: {font_size}px;
                    color: {color};
                    """)


class Image(QWidget):
    def __init__(self, display_image):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        display_image = display_image

        image = QLabel()

        pixmap = QPixmap(display_image)
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        image.setPixmap(scaled_pixmap)

        image.setScaledContents(True)
        image.setFixedSize(scaled_pixmap.size())

        self.main_layout.addWidget(image)


class SmallText(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
                font-helvetica;
                font-size: 15px;
                color: black;
                """)
