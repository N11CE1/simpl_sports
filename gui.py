import gui_prefs
import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon
# importing Qt for alignment
from prefs import write_on_exit


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
        central_widget = gui_prefs.PreferencesSelection()
        self.setCentralWidget(central_widget)

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


def clear_layout(elements):
    for child in elements.findChildren(QWidget):
        child.setParent(None)
        child.deleteLater()


def init_gui():
    # Creating the app and main window for said app
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(write_on_exit)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
