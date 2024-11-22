import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, QTextEdit, QFrame, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap


class SimplSportsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Left side: Drop-downs inside a vertical window
        left_window = QFrame()
        left_window.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        left_layout = QVBoxLayout(left_window)

        # Create a QVBoxLayout to stack text and icon vertically
        logo_layout = QVBoxLayout()

        # Text label for the logo
        logo_label = QLabel("SimplSports")
        logo_label.setFont(QFont("Arial", 20, QFont.Bold))
        logo_label.setStyleSheet("color: #2C3E50;"
                                 "border: none;")
        logo_label.setAlignment(Qt.AlignCenter)

        # Icon label
        logo_icon = QLabel()
        pixmap = QPixmap("images/logo.png")  # Path to the icon file
        logo_icon.setPixmap(pixmap)
        logo_icon.setPixmap(pixmap.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)) # Set the icon size
        logo_icon.setStyleSheet("border: none;") # Remove the border around the icon
        logo_icon.setAlignment(Qt.AlignCenter)  # Center the icon

        # Add the text and icon to the vertical layout
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(logo_icon)

        # Add the logo layout to the left layout
        left_layout.addLayout(logo_layout)

        # Add drop-down boxes
        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown4 = QComboBox()
        self.dropdown4.addItems(["Option 1", "Option 2", "Option 3"])
        self.dropdown5 = QComboBox()
        self.dropdown5.addItems(["Option 1", "Option 2", "Option 3"])

        left_layout.addWidget(self.dropdown1)
        left_layout.addWidget(self.dropdown2)
        left_layout.addWidget(self.dropdown3)
        left_layout.addWidget(self.dropdown4)
        left_layout.addWidget(self.dropdown5)

        # Right side: A vertical layout for the rest of the content
        right_layout = QVBoxLayout()

        # Header layout with buttons in the top right corner
        header_layout = QHBoxLayout()

        # Spoilers On/Off button
        self.spoilers_button = QPushButton("Spoilers: Off")
        self.spoilers_button.setStyleSheet("font-size: 12px; padding: 5px 10px;")
        self.spoilers_button.clicked.connect(self.toggle_spoilers)

        # Settings icon button
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(QPixmap("images/logo.png")))  # Download a settings icon
        self.settings_button.setStyleSheet("background-color: transparent;")
        self.settings_button.setIconSize(QSize(20, 20))

        # Spacer to push buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add the buttons to the header layout
        header_layout.addSpacerItem(spacer)
        header_layout.addWidget(self.spoilers_button)
        header_layout.addWidget(self.settings_button)

        # Add header layout to the right side layout
        right_layout.addLayout(header_layout)

        # Information boxes frame
        info_frame = QFrame()
        info_frame.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 5px;")
        info_layout = QHBoxLayout(info_frame)

        self.info_box1 = QLineEdit()
        self.info_box1.setPlaceholderText("Info Box 1")
        self.info_box2 = QLineEdit()
        self.info_box2.setPlaceholderText("Info Box 2")
        self.info_box3 = QLineEdit()
        self.info_box3.setPlaceholderText("Info Box 3")
        self.info_box4 = QLineEdit()
        self.info_box4.setPlaceholderText("Info Box 4")

        info_layout.addWidget(self.info_box1)
        info_layout.addWidget(self.info_box2)
        info_layout.addWidget(self.info_box3)
        info_layout.addWidget(self.info_box4)

        # Add the info frame to the right layout
        right_layout.addWidget(info_frame)

        # Large window layout (stacked vertically)
        large_window_layout = QVBoxLayout()  # Change to vertical layout

        # Information Window 1 - horizontal layout for 3 boxes
        self.info_window1 = QTextEdit()
        self.info_window1.setPlaceholderText('')

        # Create a horizontal layout for the 3 new windows inside Information Window 1
        horizontal_layout = QHBoxLayout()

        # First large text window
        large_window1 = QTextEdit()
        large_window1.setPlaceholderText("Large Window 1")

        # Small text window
        small_window = QTextEdit()
        small_window.setPlaceholderText("Small Window")
        small_window.setFixedWidth(100)  # Make this window very small

        # Second large text window
        large_window2 = QTextEdit()
        large_window2.setPlaceholderText("Large Window 2")

        # Add the three windows to the horizontal layout
        horizontal_layout.addWidget(large_window1)
        horizontal_layout.addWidget(small_window)
        horizontal_layout.addWidget(large_window2)

        # Add the horizontal layout to the first Information Window
        self.info_window1.setLayout(horizontal_layout)

        # Information Window 2
        self.info_window2 = QTextEdit()
        self.info_window2.setPlaceholderText("Information Window 2")

        # Add the stacked information windows (vertical layout)
        large_window_layout.addWidget(self.info_window1)
        large_window_layout.addWidget(self.info_window2)

        large_window_frame = QFrame()
        large_window_frame.setLayout(large_window_layout)
        large_window_frame.setStyleSheet("border: 1px solid #ccc; padding: 10px;")
        right_layout.addWidget(large_window_frame)

        # Combine the left and right layouts
        main_layout.addWidget(left_window, stretch=1)  # Left window takes less space
        main_layout.addLayout(right_layout, stretch=3)  # Right side takes more space

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Set main window properties
        self.setWindowTitle("SimplSports GUI")
        self.resize(1000, 600)  # Adjust size to fit all components

    def toggle_spoilers(self):
        """Toggle the spoilers button text between On and Off."""
        if self.spoilers_button.text() == "Spoilers: Off":
            self.spoilers_button.setText("Spoilers: On")
        else:
            self.spoilers_button.setText("Spoilers: Off")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SimplSportsGUI()
    main_window.show()
    sys.exit(app.exec_())
