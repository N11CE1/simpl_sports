import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

from labels.text_image_text import TextImageText


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt Window with a Button')
        self.setGeometry(100, 100, 400, 300)

        # Create a layout and set it on the window
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a button widget
        home_team = TextImageText("text", "images/logo.png", "text")

        # Add the button to the layout
        layout.addWidget(home_team)


def main():
    app = QApplication(sys.argv)

    # Create an instance of your application's GUI
    window = MainWindow()

    # Show the window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()