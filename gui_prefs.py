from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout  # importing main widget class,
# grid layout class and vertical out class
from PyQt5.QtCore import Qt  # importing Qt for alignment abilities
from prefs import user_preferences  # importing user_preferences object from prefs to read and write preferences to
import labels  # importing the labels file for use of our custom labels
import buttons  # importing the buttons file for use of our custom buttons


# defining set_sport which will be the functionality of our sports selection buttons
def set_sport(checked, key):  # takes the arguments of checked (whether the button is on or off)
    # and key (for the dictionary of our available sports
    if checked:  # checking whether button is on
        user_preferences.sports_enabled[key] = True  # setting the value of the sport matching the key given to true
        print(user_preferences.sports_enabled)  # print statements just for confirmation that the action has taken place
        print(user_preferences.sports_enabled[key])
    else:  # checking whether the button is off
        user_preferences.sports_enabled[key] = False  # setting the value of the sport matching the key to false
        print(user_preferences.sports_enabled)  # print statements again just for confirmation
        print(user_preferences.sports_enabled[key])


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
    # 2 arguments (the text to be displayed on the button and the action that clicking the button will trigger)
    nba_button = buttons.sports_button("NBA", lambda checked: set_sport(checked, "nba"))
    nfl_button = buttons.sports_button("NFL", lambda checked: set_sport(checked, "nfl"))
    nhl_button = buttons.sports_button("NHL", lambda checked: set_sport(checked, "nhl"))
    epl_button = buttons.sports_button("EPL", lambda checked: set_sport(checked, "epl"))
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


# defining preferences page 1 that will contain all the elements relevant to sports selection
def preferences_page1(clear_action):  # takes 1 argument which will be function to clear all widgets and load the next
    container = QWidget()  # creating a container that wil have everything inside it
    main_layout = QVBoxLayout(container)  # creating a vertical layout box to add organise widgets vertically
    sports_widget = sport_select()  # creating an instance of the sports selection grid
    question = labels.large_text_label("What sports do you want to follow?")  # creating a label using the large
    # text label we defined in labels.py and giving the text we want displayed as an argument
    main_layout.addWidget(question)  # adding the question to the "main_layout" vertical layout
    main_layout.addWidget(sports_widget)  # adding the sports selection grid to the "main_layout vertical layout
    next_button = buttons.push_button("Next", clear_action)  # creating a push button and passing the text
    # we want displayed on it and the action we want it to do which it gets from the argument given to the function
    main_layout.addWidget(next_button, alignment=Qt.AlignRight)  # adding the next button to the "main_layout"
    # vertical layout box and setting the alignment so it appears on the right

    return container  # returning the container to the caller
