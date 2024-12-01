from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem
from debugpy.launcher.debuggee import process

from buttons.radio_game_button import RadioGameButton
from common import shared
from common.shared import user_preferences
from labels.image import Image as Image
from labels.small_text import SmallText as SmallText
from buttons.spoiler_toggle import SpoilerToggle as SpoilerToggle
from buttons.picture_button import PictureButton as PictureButton
from widgets.game_select import GameSelection as GameSelection
from widgets.main_sport_select import SportSelection as SportSelection
from widgets.game_expanded_view import GameExpandedView as GameExpandedView
from buttons.dropdown_button import DropDownButton as DropDownButton

from api.background_worker import Update_Games_Score

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
        top_vbox = QVBoxLayout()
        right_vbox = QVBoxLayout()
        spoiler_vbox = QVBoxLayout()

        logo = Image("images/simple_sports_logo.png", 300, 165)
        week_selection = DropDownButton(week1="Week 1",week2="Week 2",week3="Week 3",week4="Week 4")
        spoilers_text = SmallText("Spoilers")
        spoilers_button = SpoilerToggle(x=42, y=22)
        prefs_button = PictureButton("images/settings.png", 48, 48, self.emit_prefs_signal)

        self.sports_selection = SportSelection()
        self.game_selection = GameSelection()
        self.game_expanded_view = GameExpandedView()

        self.sports_selection.sport_selected.connect(self.game_selection.update_games)
        self.game_selection.game_selected.connect(self.game_expanded_view.update_game)
        spoilers_button.spoiler_toggled.connect(self.game_selection.spoiler_toggled)
        spoilers_button.spoiler_toggled.connect(self.game_expanded_view.spoiler_toggled)

        self.sports_selection.emit_current_sport()
        top_spacer = QSpacerItem(360, 0)
        left_vbox.addWidget(logo, alignment=Qt.AlignLeft)
        left_vbox.addWidget(self.sports_selection)
        spoiler_vbox.addWidget(spoilers_button)
        spoiler_vbox.addWidget(spoilers_text)
        dropdown_spacer = QSpacerItem(0, 0)
        top_vbox.addSpacerItem(dropdown_spacer)
        top_vbox.addWidget(week_selection)
        top_hbox.addLayout(top_vbox)
        top_hbox.addSpacerItem(top_spacer)
        top_hbox.addLayout(spoiler_vbox)
        top_hbox.setAlignment(spoiler_vbox, Qt.AlignRight)
        top_hbox.addWidget(prefs_button)
        right_vbox.addLayout(top_hbox)
        right_vbox.addWidget(self.game_selection)
        right_vbox.addWidget(self.game_expanded_view)
        right_vbox.setSpacing(0)
        right_vbox.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(left_vbox)
        self.main_layout.addLayout(right_vbox)

        # Background task for updating schedule, game scores, and standings
        self.proc_update_game_score = Update_Games_Score()
        self.proc_update_game_score.update_ui.connect(self.update_from_worker)
        self.proc_update_game_score.start()

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
        # print("preferences button clicked")
        self.prefs_button_clicked.emit()

    def emit_current_sport(self):
        pass

    def update_from_worker(self):
        self.game_selection.update_ui_scores(shared.current_sport)

    def closeEvent(self, event):
        """Override closeEvent to clean up worker thread on application close."""
        if self.proc_update_game_score is not None:
            if self.proc_update_game_score.isRunning():
                print("Worker thread is running. Stopping it now...")
                self.proc_update_game_score.quit()
        event.accept()