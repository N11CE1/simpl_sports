import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QComboBox

from labels.text_image_text import TextImageText
from buttons.radio_sports_button import RadioSportsButton as RadioSportsButton


from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class DropDownWidget(QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        layout = QVBoxLayout()

        self.combo = QComboBox()

        for arg_name, arg_value in kwargs.items():
            if arg_value is not None:
                print(arg_name, arg_value)
                self.combo.addItem(arg_value)

        self.combo.currentIndexChanged.connect(self.on_selection_change)

        layout.addWidget(self.combo)
        self.setLayout(layout)

    def on_selection_change(self):
        pass


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
        # home_team = TextImageText("text", "images/logo.png", "text")
        dropdown = DropDownWidget(week1="week 1", week2="week 2", week3="week 3", week4="week 4")
        # Add the button to the layout
        layout.addWidget(dropdown)


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