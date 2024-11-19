import gui_prefs
import gui_main
import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon

import shared
# importing Qt for alignment
from prefs import write_on_exit
from shared import user_preferences


class MainWindow(QMainWindow):
    def __init__(self):
        # Inheriting from the superclass
        super().__init__()
        # Setting window name and size
        self.setWindowTitle('Simpl Sports')
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("background-color: #FFFFFF;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.prefs_ui = gui_prefs.PreferencesSelection()
        self.main_ui = gui_main.MainMenu()
        # setting page to preferences page 1
        self.central_widget.addWidget(self.main_ui)
        self.central_widget.addWidget(self.prefs_ui)

        self.prefs_ui.next_button_clicked.connect(self.show_main_ui)
        self.main_ui.prefs_button_clicked.connect(self.show_prefs_ui)
        if not shared.prefs_existed:
            self.show_prefs_ui()
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

    def show_main_ui(self):
        self.main_ui.set_main_layout()
        self.central_widget.setCurrentWidget(self.main_ui)


    def show_prefs_ui(self):
        self.prefs_ui.reset_to_page1()
        self.central_widget.setCurrentWidget(self.prefs_ui)


def clear_layout(elements):
    for child in elements.findChildren(QWidget):
        child.setParent(None)
        child.deleteLater()


def init_gui():
    # Creating the app and main window for said app
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: write_on_exit(user_preferences))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


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