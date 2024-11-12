from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGridLayout

import buttons


def sport_select():
    container = QWidget()
    sports_grid = QGridLayout()
    sports_grid.setContentsMargins(100, 100, 100, 100)

    nba_label = buttons.sports_button("NBA")
    nfl_label = buttons.sports_button("NFL")
    nhl_label = buttons.sports_button("NHL")
    epl_label = buttons.sports_button("EPL")

    sports_grid.addWidget(nba_label, 0, 0)
    sports_grid.addWidget(nfl_label, 0, 1)
    sports_grid.addWidget(nhl_label, 1, 0)
    sports_grid.addWidget(epl_label, 1, 1)


    container.setLayout(sports_grid)

    return container

