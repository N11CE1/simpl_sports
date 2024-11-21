from PyQt5.QtWidgets import QPushButton


class PushButton(QPushButton):
    def __init__(self, text, action):
        super().__init__(text)
        self.clicked.connect(action)
        self.setFixedSize(150, 80)
        self.setStyleSheet("""
            color: black;
            background-color: #F5F5F5;
            font: helvetica;
            font-size: 30px;
            border: 2px solid #D9D9D9;
            border-radius: 15px;
            """)