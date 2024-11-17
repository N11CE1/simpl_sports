from PyQt5.QtWidgets import QWidget, QHBoxLayout


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout()
