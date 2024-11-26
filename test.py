import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame

from labels.text_image_text import TextImageText
from buttons.radio_sports_button import RadioSportsButton as RadioSportsButton


from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class StatsLabel(QFrame):
    def __init__(self, **kwargs):
        super().__init__()
        self.setObjectName('StatsLabel')
        self.setStyleSheet(self.false_style())  # set false style as default style
        self.vert_box = QVBoxLayout()
        print(kwargs)
        for arg_name, arg_value in kwargs.items():
            if arg_value is not None:
                print(arg_name, arg_value)
                label = QLabel(arg_value)
                self.vert_box.addWidget(label)
        self.setLayout(self.vert_box)


    @staticmethod
    def false_style():
        return """
                    color: black;
                    background-color: #F5F5F5;
                    font: helvetica;
                    font-size: 50px;
                    border: 2px solid #D9D9D9;
                    border-radius: 15px;
                

                """





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
        element = StatsLabel(text1="hello", text2="world", text3="yes", stat4="indeed")
        # Add the button to the layout
        layout.addWidget(element)


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