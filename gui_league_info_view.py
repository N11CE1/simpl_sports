"""

POC for passing data from one form to another

"""
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
import datasets as da

class LeagueInformationViewForm(QWidget):
    def __init__(self, league_id, pixmap=None):
        super().__init__()
        self.league_id = league_id

        # Set the title and dimensions of the window
        self.setWindowTitle("League Information")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(1000, 500)

        # Get the screen's dimensions
        screen_geometry = self.screen().availableGeometry()  # Available screen geometry (excluding taskbars)
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Get the size of the window
        window_width = self.width()
        window_height = self.height()

        # Calculate the position for the window to be centered
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Move the window to the calculated position
        self.move(x, y)

        self.header = QLabel(self)
        self.header.setFixedHeight(60)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet(
            """
            QLabel {
                border: 2px solid white;
                font-size: 36px;
                font-weight: bold;
            }
            """
        )

        self.badge = QLabel("badge")
        self.badge.setFixedSize(300, 300)
        self.badge.setAlignment(Qt.AlignCenter)

        if pixmap:
            self.badge.setPixmap(pixmap)

        self.header.setText(da.leagues['name'].iloc[int(self.league_id)])
        print(da.leagues.columns)

        parent_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        info_layout = QGridLayout()

        header_layout.addWidget(self.header)
        info_layout.addWidget(self.badge)
        parent_layout.addLayout(header_layout)
        parent_layout.addLayout(info_layout)

        self.setLayout(parent_layout)

    def set_badge(self, label_src: QLabel):
        # label_dest.setPixmap(QPixmap(label_src.pixmap()))
        self.badge.setPixmap(QPixmap(label_src.value()))