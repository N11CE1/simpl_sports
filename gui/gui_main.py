from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem

from labels.image import Image as Image
from labels.small_text import SmallText as SmallText
from buttons.spoiler_toggle import SpoilerToggle as SpoilerToggle
from buttons.picture_button import PictureButton as PictureButton
from widgets.game_select import GameSelection as GameSelection
from widgets.main_sport_select import SportSelection as SportSelection
from widgets.game_expanded_view import GameExpandedView as GameExpandedView

class MainMenu(QWidget):

    prefs_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.sports_selection = None
        self.game_selection = None
        self.game_expanded_view = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.set_main_layout()


    def set_main_layout(self):
        self.clear_layout(self.main_layout)

        left_vbox = QVBoxLayout()
        top_hbox = QHBoxLayout()
        right_vbox = QVBoxLayout()
        spoiler_vbox = QVBoxLayout()

        logo = Image("images/logo.png")
        spoilers_text = SmallText("Spoilers")
        spoilers_button = SpoilerToggle(x=42, y=22)
        prefs_button = PictureButton("images/settings.png", 48, 48, self.emit_prefs_signal)

        self.sports_selection = SportSelection()
        self.game_selection = GameSelection()
        self.game_expanded_view = GameExpandedView()
        self.sports_selection.sport_selected.connect(self.game_selection.update_games)
        # self.game_selection.game_selected.connect(self.game_expanded_view.update_game)
        top_spacer = QSpacerItem(600, 20)
        left_vbox.addWidget(logo, alignment=Qt.AlignLeft)
        left_vbox.addWidget(self.sports_selection)
        spoiler_vbox.addWidget(spoilers_button)
        spoiler_vbox.addWidget(spoilers_text)
        top_hbox.addSpacerItem(top_spacer)
        top_hbox.addLayout(spoiler_vbox)
        top_hbox.setAlignment(spoiler_vbox, Qt.AlignRight)
        top_hbox.addWidget(prefs_button)
        right_vbox.addLayout(top_hbox)
        right_vbox.addWidget(self.game_selection)
        right_vbox.addWidget(self.game_expanded_view)
        self.main_layout.addLayout(left_vbox)
        self.main_layout.addLayout(right_vbox)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
            else:
                pass

    def emit_prefs_signal(self):
        print("preferences button clicked")
        self.prefs_button_clicked.emit()






