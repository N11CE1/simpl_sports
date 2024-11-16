from PyQt5.QtWidgets import QLabel  # importing QLabel to be the basis of our labels
from PyQt5.QtCore import Qt  # importing Qt for alignment abilities


# creating a default large test label to be reused wherever needed
def large_text_label(text):  # takes argument of text for easy customisation
    label = QLabel(text)  # our label will be an object of the pre-configured class QLabel
    label.setAlignment(Qt.AlignCenter)  # setting text alignment so label contents are always centered
    label.setStyleSheet("""
                font-helvetica;
                font-size: 40px;
                color: black;
                """)  # using style sheet to set visual properties
    return label  # returning our label to the caller
