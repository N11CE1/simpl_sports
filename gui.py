import buttons
import gui_prefs
import labels
import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon, QPixmap, QFont
# importing Qt for alignment
from PyQt5.QtCore import Qt
from prefs import write_on_exit
from gui_prefs import save_sport_num


class MainWindow(QMainWindow):
    def __init__(self):
        # Inheriting from the superclass
        super().__init__()
        # Setting window name and size
        self.setWindowTitle('Simpl Sports')
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("background-color: #FFFFFF;")

        # setting page to preferences page 1
        page = gui_prefs.preferences_page1(self.clear_layout)
        self.setCentralWidget(page)

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

    def clear_layout(self):
        pass


def init_gui():
    # Creating the app and main window for said app
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(write_on_exit)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
