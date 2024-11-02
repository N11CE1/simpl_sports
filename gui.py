import sys
# Importing QApplication for the main application QMain Window for the window
# and QLabel for objects within the window
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# Importing QIcon for window icon, QPixmap for images withing the app
# and QFont for font in the app
from PyQt5.QtGui import QIcon, QPixmap, QFont
# importing Qt for alignment
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        # Inheriting from the superclass
        super().__init__()
        # Setting window name and size
        self.setWindowTitle('Simpl Sports')
        self.setFixedSize(1400, 1000)
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet("background-color: #FFFFFF;")

        label = QLabel("AFL", self)
        label.setFont(QFont('Arial', 30))
        label.setGeometry(50, 425, 294, 109)
        label.setStyleSheet("font-weight: bold;"
                            "color: black;"
                            "background color: #F5F5F5;"
                            "border: 2px solid #D9D9D9;"
                            "border-radius: 8px;"
                            "padding: 10px;")
        label.setAlignment(Qt.AlignCenter)

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


def init_gui():
    # Creating the app and main window for said app
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
