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