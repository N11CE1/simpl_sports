from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QButtonGroup
from common import shared
from buttons.radio_sports_button import RadioSportsButton


class SportSelection(QWidget):
    SCROLL_AREA_STYLE = """  
            QScrollArea {
            border: 2px solid #ccc;
            border-radius: 10px;
            background: transparent;
            padding-right: 0px;
            }
            
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            
            QScrollBar:horizontal {
                border: none;
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
            
            QScrollBar:vertical {
                width: 10px;
                background: transparent;
                border-radius: 4px;
                margin-top: 5px;
                margin-bottom: 5px;
                margin-right: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: #888;
                min-width: 6px;
                border-radius: 3px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
            QScrollBar::left-arrow:vertical, QScrollBar::right-arrow:vertical {
                background: transparent;
                background-color: transparent;
                background-image: none;
                border: none;
                width: 0px;
                height: 0px;
                margin: 0px;
                padding: 0px;
            }
            """

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        scroll_area = self._create_styled_scroll_area()
        self.main_layout.addWidget(scroll_area)
        container = QWidget(self)
        self.sports_buttons_layout = QVBoxLayout()
        container.setLayout(self.sports_buttons_layout)
        scroll_area.setWidget(container)
        self.sports_button_group = QButtonGroup()
        self.sports_button_group.setExclusive(True)
        self.update_sports()

    def _create_styled_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(290)
        scroll_area.setMaximumHeight(400)
        self._style_scroll_area(scroll_area)
        return scroll_area

    def _style_scroll_area(self, scroll_area):
        scroll_area.setStyleSheet(self.SCROLL_AREA_STYLE)

    def update_sports(self):
        while self.sports_buttons_layout.count():
            item = self.sports_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget:
                self.sports_button_group.removeButton(widget)
                widget.deleteLater()
        for sports in shared.user_preferences.sports_order.values():
            radio_button = RadioSportsButton(sports.upper())
            self.sports_button_group.addButton(radio_button)
            self.sports_buttons_layout.addWidget(radio_button)
