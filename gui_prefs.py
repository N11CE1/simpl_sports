from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QListWidget, \
    QAbstractItemView, QListWidgetItem, QLabel  # importing main widget class,
# grid layout class and vertical out class
from PyQt5.QtCore import Qt  # importing Qt for alignment abilities
import labels  # importing the labels file for use of our custom labels
import buttons  # importing the buttons file for use of our custom buttons
from shared import user_preferences


class PreferencesSelection(QWidget):  # creating preference selection as a class using QWidget as a base to customise
    def __init__(self):  # initialising class
        super().__init__()  # calling super to give class all properties of QWidgets
        self.main_layout = None  # adding main layout attribute which will have everything in it
        self.init_ui()  # triggering init_ui

    def init_ui(self):  # sets the start point of the ui when an object of this class is triggered
        self.main_layout = QVBoxLayout()  # the main layout will be
        self.setLayout(self.main_layout)
        self.preferences_page1()

    # defining preferences page 1 that will contain all the elements relevant to sports selection
    def preferences_page1(self):  # takes argument which will be function to clear all widgets and load the next
        self.clear_layout(self.main_layout)
        sports_widget = sport_select()  # creating an instance of the sports selection grid
        question = labels.large_text_label("What sports do you want to follow?")  # creating a label using the large
        # text label we defined in labels.py and giving the text we want displayed as an argument
        self.main_layout.addWidget(question)  # adding the question to the "main_layout" vertical layout
        self.main_layout.addWidget(sports_widget)  # adding the sports selection grid to the "main_layout vertical layout
        next_button = buttons.push_button("Next", self.page1_next_click)  # creating a push button and passing the text
        # we want displayed on it and the action we want it to do which it gets from the argument given to the function
        self.main_layout.addWidget(next_button, alignment=Qt.AlignRight)  # adding the next button to the "main_layout"
        # vertical layout box and setting the alignment, so it appears on the right

    def preferences_page2(self):
        self.clear_layout(self.main_layout)
        title_text = labels.large_text_label("Order your selected sport from most to least important")
        title_text.setAlignment(Qt.AlignCenter)
        selected_items = self.get_selected_sports()
        self.order_list = OrderList(selected_items)
        next_button = buttons.push_button("Next", self.page2_next_click)
        self.main_layout.addWidget(title_text)
        self.main_layout.addWidget(self.order_list)
        self.main_layout.addWidget(next_button, alignment=Qt.AlignRight)


    def page1_next_click(self):
        self.preferences_page2()

    def page2_next_click(self):
        user_preferences.sports_order = self.order_list.get_order_list()
        self.clear_layout(self.main_layout)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def get_selected_sports(self):
        selected_items = []
        for key, enabled in user_preferences.sports_enabled.items():
            if enabled:
                display_text = key.upper()
                selected_items.append({"display_text": display_text, "unique_key": key})
        return selected_items


# defining set_sport which will be the functionality of our sports selection buttons
def set_sport(checked, key):  # takes the arguments of checked (whether the button is on or off)
    user_preferences.sports_enabled[key] = checked
    print(user_preferences.sports_enabled)


# save_sport_num function will set the order the sports are displayed in, hasn't been written yes
def save_sport_num():
    pass


# creating the grid that will house all the sports selection buttons
def sport_select():
    container = QWidget()  # creating a widget that will contain the grid layout
    sports_grid = QGridLayout()  # creating the grid
    sports_grid.setContentsMargins(100, 100, 100, 100)  # setting the margins on the grid (for looks mostly)

    # creating a button for each sport in the sports selection screen
    # because each button is on object of the sports_button class we defined in buttons.py they each take
    # 3 arguments (the dictionary key to affect the state of the correct sport,
    # the text to be displayed on the button and the action that clicking the button will trigger)
    nba_button = buttons.sports_button("nba", "NBA", lambda checked: set_sport(checked, "nba"))
    nfl_button = buttons.sports_button("nfl", "NFL", lambda checked: set_sport(checked, "nfl"))
    nhl_button = buttons.sports_button("nhl", "NHL", lambda checked: set_sport(checked, "nhl"))
    epl_button = buttons.sports_button("epl", "EPL", lambda checked: set_sport(checked, "epl"))
    # lambda just allow me to define and execute code on 1 line
    # in this case it calls the set_sport function and passes the
    # checked status and the key to search the sport dictionary for

    # adding each button to the grid layout and defining their position in the grid
    sports_grid.addWidget(nba_button, 0, 0)
    sports_grid.addWidget(nfl_button, 0, 1)
    sports_grid.addWidget(nhl_button, 1, 0)
    sports_grid.addWidget(epl_button, 1, 1)

    # adding the grid to the container we created before
    container.setLayout(sports_grid)

    return container  # return the container, that contains everything we've done in this function, to the caller


class OrderList(QListWidget):  # creating order list class
    def __init__(self, items, parent=None):  # giving attributes of items and parent
        # which defaults to non because it is optional
        super().__init__(parent)  # inherits properties of QListWidget
        self.setAcceptDrops(True)  # allowing to accept drag and drop
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.data_dict = {}  # dictionary data will be stored in
        self.set_items(items)

    def set_items(self, items):  # setting default order of list
        self.clear()  # clearing any existing items
        for item in items:
            list_item = QListWidgetItem(item["display_text"])
            list_item.setData(Qt.UserRole, item["unique_key"])
            self.addItem(list_item)
        self.update_data()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.update_data()
        event.accept()

    def update_data(self):  # updating dictionary
        self.data_dict = {}
        for index in range(self.count()):
            item = self.item(index)
            unique_key = item.data(Qt.UserRole)
            self.data_dict[index] = unique_key
        print("dictionary:", self.data_dict)

    def get_order_list(self):
        return self.data_dict
