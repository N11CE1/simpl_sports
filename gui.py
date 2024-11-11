from prefs import user_prefs
import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QLabel, QScrollArea
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon, QPixmap, QFont
# importing Qt for alignment
from PyQt5.QtCore import Qt

import prefs

'''
class MainWindow(QMainWindow):
    def __init__(self):
        # Inheriting from the superclass
        super().__init__()
        # Setting window name and size
        self.setWindowTitle('Simpl Sports')
        self.setFixedSize(1400, 1000)
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("background-color: #FFFFFF;")

        afl = QLabel("AFL", self)
        sport_button(afl, 50, 284)
        nrl = QLabel("NRL", self)
        sport_button(nrl, 50, 425)
        a_league = QLabel("A League", self)
        sport_button(a_league, 50, 566)
        nba = QLabel("NBA", self)
        sport_button(nba, 50, 707)
        nhl = QLabel("NHL", self)
        sport_button(nhl, 50, 848)



        # Window centering method
        self.center()

    def center(self):
        # fetching the screen's geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculating the middle
        screen_center_x = screen_geometry.width() // 2
        screen_center_y = screen_geometry.height() // 2

        # Calculating window geometry to be in the middle
        window_x = screen_center_x - (self.width() // 2)
        window_y = screen_center_y - (self.height() // 2)

        # Moving window to dead centre of screen
        self.move(window_x, window_y)

'''
def init_gui():
    # Creating the app and main window for said app
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
'''

def sport_button(sport, x_pos, y_pos):
    sport.setFont(QFont('Arial', 30))
    sport.setGeometry(x_pos, y_pos, 294, 109)
    sport.setStyleSheet("""
                        QLabel {
                            font-weight: bold;
                            color: black;
                            background-color: #F5F5F5;
                            border: 2px solid #D9D9D9;
                            border-radius: 8px;
                            padding: 10px;
                            }
                        QLabel:hover {
                            background-color: #007AFF;
                            border: 2px solid #007AFF;
                            }
                        QLabel:pressed {
                            background-color: #FFFFFF;
                            border: 2px solid #007AFF;
                            }
                        """)
    sport.setAlignment(Qt.AlignCenter)
'''
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scrollable List of Labels')
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout to hold the scroll area
        layout = QVBoxLayout(self)

        # Create a QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Create a QWidget to act as a container for the labels
        container = QWidget()
        scroll_area.setWidget(container)

        # Create a QVBoxLayout for the container
        container_layout = QVBoxLayout(container)

        # Add multiple QLabel widgets to the container
        for i in range(1, user_prefs.sports_num):
            label = QLabel(f'Label {i}', self)
            container_layout.addWidget(label)