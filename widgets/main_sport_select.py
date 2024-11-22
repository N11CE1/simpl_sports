from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QButtonGroup
from common import shared
from buttons.radio_sports_button import RadioSportsButton


class SportSelection(QWidget):
    SCROLL_AREA_STYLE = """  
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 12px;
                margin: 0px 0px 0px 0px;
                padding: 0px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
            """

    def __init__(self):
        super().__init__()
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
        scroll_area.setMaximumWidth(400)
        scroll_area.setMaximumHeight(500)
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
