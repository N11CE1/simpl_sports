from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from labels.image_with_text import ImageWithText as ImageWithText
from labels.image import Image as Image
from labels.small_text import SmallText as SmallText


class GameExpandedView(QWidget):
    def __init__(self):
        super().__init__()
        self.container = None
        self.score_layout = None
        self.statistics_layout = None
        self.team1 = None
        self.vs = None
        self.team2 = None
        self.stat1 = None
        self.stat2 = None
        self.stat3 = None
        self.stat4 = None
        self.setFixedSize(800, 500)
        self.setStyleSheet("border: 1px solid black;")
        self.init_ui()

    def init_ui(self):

        self.team1 = ImageWithText("images/logo.png", "Team 1")
        self.vs = Image("images/logo.png")
        self.team2 = ImageWithText("images/logo.png", "Team 2")

        self.score_layout = QHBoxLayout()
        self.score_layout.addWidget(self.team1)
        self.score_layout.addWidget(self.vs)
        self.score_layout.addWidget(self.team2)

        self.stat1 = SmallText("State 1 Here")
        self.stat2 = SmallText("State 2 Here")
        self.stat3 = SmallText("State 3 Here")
        self.stat4 = SmallText("State 4 Here")

        self.statistics_layout = QGridLayout()
        self.statistics_layout.addWidget(self.stat1, 0, 0)
        self.statistics_layout.addWidget(self.stat2, 0, 1)
        self.statistics_layout.addWidget(self.stat3, 1, 0)
        self.statistics_layout.addWidget(self.stat4, 1, 1)

        self.container = QVBoxLayout()
        self.container.addLayout(self.score_layout)
        self.container.addLayout(self.statistics_layout)
        self.setLayout(self.container)