from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLabel

from buttons.toggle_button import ToggleButton


class RadioGameButton(ToggleButton):
    def __init__(self, date=None, home=None, home_score=None, away=None, away_score=None, time=None, action=None):
        super().__init__(action)
        self.set_font()
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
            items.setStyleSheet(self.set_font())

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
    def set_font():
        return """
        font: helvetica;
        font-size: 20px;
        color: black;
        background-color: transparent;
        """