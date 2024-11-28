from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


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
                label.setAlignment(Qt.AlignCenter)
                self.vert_box.addWidget(label)
        self.vert_box.setAlignment(Qt.AlignCenter)
        self.setLayout(self.vert_box)

    @staticmethod
    def false_style():
        return """
                    QFrame{
                        font: helvetica;
                        border: 2px solid #D9D9D9;
                        border-radius: 15px;
                    }
                    QLabel{
                        color: black;
                        background-color: white;
                        font-size: 20px;
                        border: none;
                    }
                """