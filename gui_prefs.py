from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QListWidget, \
    QAbstractItemView, QListWidgetItem, QHBoxLayout, QScrollArea, QButtonGroup, QSpacerItem
from PyQt5.QtCore import Qt, QSize, pyqtSignal
import labels
import buttons
from shared import user_preferences, default_prefs


class PreferencesSelection(QWidget):

    next_button_clicked = pyqtSignal()
    preferences_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.hbox = None
        self.right_vbox = None
        self.left_vbox = None
        self.order_list = None
        self.spoiler_buttons = None
        self.spoiler_button_group = None
        self.page1_buttons_box = None
        self.page2_buttons_box = None
        self.page2_back_button = None
        self.page2_next_button = None
        self.not_enough = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.preferences_page1()

    def preferences_page1(self):
        self.clear_layout(self.main_layout)
        sports_widget = sport_select()
        question = labels.CustomLabel("What sports do you want to follow?", 40, "black")
        question.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.not_enough = labels.CustomLabel("You need to select at least 2 sports", 40, "black")
        self.not_enough.setStyleSheet("""
                                 color: transparent;
                                 font-size: 30px;
                                 """)
        self.main_layout.addSpacing(100)
        self.main_layout.addWidget(question)
        self.main_layout.addWidget(self.not_enough)
        self.main_layout.addWidget(
            sports_widget)

        self.page1_buttons_box = QHBoxLayout()
        self.main_layout.addLayout(self.page1_buttons_box)
        skip_button = buttons.push_button(f"SKIP\n(use defaults) ", self.skip_button_action)
        skip_button.setFixedSize(250, 100)
        skip_button.clicked.connect(self.emit_next_signal)
        page1_next_button = buttons.push_button("Next", self.page1_next_click)
        self.page1_buttons_box.addWidget(skip_button, alignment=Qt.AlignLeft)
        self.page1_buttons_box.addWidget(page1_next_button, alignment=Qt.AlignRight)

    @staticmethod
    def skip_button_action():
        user_preferences.sports_enabled = default_prefs.sports_enabled
        user_preferences.sports_order = default_prefs.sports_order
        user_preferences.spoilers = default_prefs.spoilers

    def page1_next_click(self):
        selected_sports_count = sum(1 for key, value in user_preferences.sports_enabled.items() if value)
        if selected_sports_count > 1:
            print(selected_sports_count)
            self.preferences_page2()
        else:
            self.not_enough.setStyleSheet("""
                                          color: red;
                                          font-size: 30px;
                                          """)

    def preferences_page2(self):
        self.clear_layout(self.main_layout)

        order_text = labels.CustomLabel("Order your selected sport"
                                        "\nfrom most to least important", 40)
        spoiler_text = labels.CustomLabel("Do you want spoilers"
                                          "\nenabled for live games?", 40)

        selected_items = self.get_selected_sports()
        self.order_list = OrderList(selected_items)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.order_list)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)

        self.page2_buttons_box = QHBoxLayout()
        self.page2_back_button = buttons.push_button("Back", self.go_back)
        self.page2_next_button = buttons.push_button("Save", self.page2_next_click)
        self.page2_next_button.clicked.connect(self.emit_next_signal)

        self.page2_buttons_box.addWidget(self.page2_back_button, alignment=Qt.AlignLeft)
        self.page2_buttons_box.addWidget(self.page2_next_button, alignment=Qt.AlignRight)

        self.spoiler_button_group = QButtonGroup(self)
        self.spoiler_button_group.setExclusive(True)
        spoiler_on = buttons.SpoilersButton(
            "Spoilers On",
            action=lambda checked: setattr(user_preferences, "spoilers", True))
        spoiler_on.setChecked(user_preferences.spoilers)
        spoiler_off = buttons.SpoilersButton(
            "Spoilers Off",
            action=lambda checked: setattr(user_preferences, "spoilers", False))
        spoiler_off.setChecked(not user_preferences.spoilers)
        self.spoiler_button_group.addButton(spoiler_on)
        self.spoiler_button_group.addButton(spoiler_off)

        self.left_vbox = QVBoxLayout()
        self.left_vbox.addWidget(order_text, alignment=(Qt.AlignTop | Qt.AlignHCenter))
        self.left_vbox.addWidget(self.order_list, alignment=Qt.AlignCenter)

        self.right_vbox = QVBoxLayout()
        right_vbox_spacer1 = QSpacerItem(0, 120)
        self.right_vbox.addWidget(spoiler_text, alignment=(Qt.AlignTop | Qt.AlignHCenter))
        self.right_vbox.addSpacerItem(right_vbox_spacer1)
        self.right_vbox.addWidget(spoiler_on, alignment=Qt.AlignCenter)
        self.right_vbox.addWidget(spoiler_off, alignment=Qt.AlignCenter)
        right_vbox_spacer2 = QSpacerItem(0, 120)
        self.right_vbox.addSpacerItem(right_vbox_spacer2)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.left_vbox)
        spacer_item = QSpacerItem(100, 0)
        self.hbox.addSpacerItem(spacer_item)
        self.hbox.addLayout(self.right_vbox)
        self.hbox.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setLayout(self.hbox)

        self.main_layout.addWidget(container)
        buttons_container = QWidget()
        buttons_container.setLayout(self.page2_buttons_box)
        self.main_layout.addWidget(buttons_container)

    def go_back(self):
        self.preferences_page1()

    def page2_next_click(self):
        user_preferences.sports_order = self.order_list.get_order_list()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    @staticmethod
    def get_selected_sports():
        selected_items = []
        for key, enabled in user_preferences.sports_enabled.items():
            if enabled:
                display_text = key.upper()
                selected_items.append({"display_text": display_text, "unique_key": key})
        return selected_items

    def reset_to_page1(self):
        self.preferences_page1()

    def emit_next_signal(self):
        self.next_button_clicked.emit()


def set_sport(checked, key):
    user_preferences.sports_enabled[key] = checked
    print(user_preferences.sports_enabled)


def sport_select():
    container = QWidget()
    sports_grid = QGridLayout()
    sports_grid.setContentsMargins(100, 100, 100, 100)

    nba_button = buttons.sports_button("nba", "NBA", lambda checked: set_sport(checked, "nba"))
    nfl_button = buttons.sports_button("nfl", "NFL", lambda checked: set_sport(checked, "nfl"))
    nhl_button = buttons.sports_button("nhl", "NHL", lambda checked: set_sport(checked, "nhl"))
    epl_button = buttons.sports_button("epl", "EPL", lambda checked: set_sport(checked, "epl"))

    sports_grid.addWidget(nba_button, 0, 0)
    sports_grid.addWidget(nfl_button, 0, 1)
    sports_grid.addWidget(nhl_button, 1, 0)
    sports_grid.addWidget(epl_button, 1, 1)

    container.setLayout(sports_grid)

    return container


class OrderList(QListWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.user_preferences_updated = None
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.data_dict = {}
        self.setFixedSize(300, 500)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 5px solid #D9D9D9;
                border-radius: 20px;
                font-size: 30px;
            }
            QListWidget::item {
                color: black;
                background-color: #F5F5F5;
                border: 2px solid #D9D9D9;
                border-radius: 15px;
                padding: 10px;    
            }
            QListWidget::item:selected {
                border: 2px solid #007AFF;
                border-radius: 15px;
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
        """)
        self.set_items(items)

    def set_items(self, items):
        self.clear()
        for item in items:
            list_item = QListWidgetItem(item["display_text"])
            list_item.setData(Qt.UserRole, item["unique_key"])
            list_item.setTextAlignment(Qt.AlignCenter)
            list_item.setSizeHint(QSize(30, 100))
            self.addItem(list_item)
        self.update_data()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.update_data()
        event.accept()

    def update_data(self):
        self.data_dict = {}
        for index in range(self.count()):
            item = self.item(index)
            unique_key = item.data(Qt.UserRole)
            self.data_dict[index] = unique_key
        print("dictionary:", self.data_dict)

    def get_order_list(self):
        return self.data_dict

    def update_user_preferences(self):
        self.user_preferences_updated.emit()
