from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox

CSS_STYLE = """
    color: black;
    background-color: transparent;
    border: 1px solid #D9D9D9;
    border-radius: 5px;
"""

class DropDownButton(QWidget):
    def __init__(self, **kwargs):
        super().__init__()
        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.setStyleSheet(CSS_STYLE)

        for arg_name, arg_value in kwargs.items():
            if arg_value is not None:
                print(arg_name, arg_value)
                self.combo.addItem(arg_value)

        self.combo.currentIndexChanged.connect(self.on_selection_change)

        layout.addWidget(self.combo)
        self.setLayout(layout)

    def on_selection_change(self):
        pass
