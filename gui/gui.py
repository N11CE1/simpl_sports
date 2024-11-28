import gui.gui_prefs as gui_prefs
import gui.gui_main as gui_main
import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon

from common import shared
# importing Qt for alignment
from prefs import write_on_exit
from common.shared import user_preferences

from api import initialize_new_installed_app as new_app
from api import data_operations as do

class MainWindow(QMainWindow):
    def __init__(self):
        # Inheriting from the superclass
        super().__init__()

        # Setting window name and size
        self.setWindowTitle('Simpl Sports')
        self.setFixedSize(1200, 800)
        self.setWindowIcon(QIcon('../images/logo.png'))
        self.setStyleSheet("background-color: #FFFFFF;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        ## Initialize database when very first run of app
        do.initialize_tables()
        if len(do.get_leagues()) == 0:
            initialize_window = new_app.LoadingWindow()
            initialize_window.exec()

        self.prefs_ui = gui_prefs.PreferencesSelection()
        self.main_ui = gui_main.MainMenu()
        # setting page to preferences page 1
        self.central_widget.addWidget(self.main_ui)
        self.central_widget.addWidget(self.prefs_ui)

        self.prefs_ui.next_button_clicked.connect(self.show_main_ui)
        self.main_ui.prefs_button_clicked.connect(self.show_prefs_ui)
        if not shared.prefs_existed:
            self.show_prefs_ui()

        # Window centering method
        self.center()



    def center(self):
        # fetching the screen's geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()

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
