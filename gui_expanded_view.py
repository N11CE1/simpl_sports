import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from functools import partial
import data_operations as do
import random

class SimpleForm(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title and dimensions of the window
        self.setWindowTitle("Expanded View")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(1000, 800)

        # move the form to the center on start-up
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)

        # Create widgets

        # Create a QLabel to display the image
        self.image_home_team = QLabel(self)
        self.image_home_team.setFixedSize(300, 300)
        self.image_home_team.setAlignment(Qt.AlignCenter)

        self.image_away_team = QLabel(self)
        self.image_away_team.setFixedSize(300, 300)
        self.image_away_team.setAlignment(Qt.AlignCenter)

        self.image_vs_pixmap = QPixmap('vs image.png')
        self.image_vs = QLabel(self)
        self.image_vs.setAlignment(Qt.AlignCenter)
        self.image_vs.setPixmap(self.image_vs_pixmap)
        self.image_vs.setFixedSize(200, 300)

        # Create layout
        # Title Grid
        parent_layout = QVBoxLayout()
        title_layout = QGridLayout()
        images_layout = QGridLayout()
        other_info_layout = QGridLayout()

        # layout = QGridLayout (self)
        images_layout.addWidget(self.image_home_team, 0, 0)
        images_layout.addWidget(self.image_vs, 0, 1)
        images_layout.addWidget(self.image_away_team, 0, 2)

        # other_info_layout.addWidget(self.test_label, 1, 0)

        parent_layout.addLayout(title_layout)
        parent_layout.addLayout(images_layout)
        parent_layout.addLayout(other_info_layout)

        self.setLayout(parent_layout)
        print(self.image_vs.pos())

        # Start loading the image

        # get image from database randomize from 30 teams
        home_team = do.get_team_badge(random.randint(0, 29))
        away_team = do.get_team_badge(random.randint(0, 29))

        self.load_image_from_web(self.image_home_team,home_team)
        self.load_image_from_web(self.image_away_team,away_team)

    def load_image_from_web(self, label: QLabel, url):
        # Create a QNetworkAccessManager
        self.manager = QNetworkAccessManager(self)

        # Connect the finished signal to a method that handles the response
        self.manager.finished.connect(partial(self.on_image_downloaded, img_label=label))

        # Create a QNetworkRequest
        request = QNetworkRequest(QUrl(url))

        # Send the request to download the image
        self.manager.get(request)

    def on_image_downloaded(self, reply, img_label: QLabel):
        # print(reply)
        if reply.error() == reply.NoError:
            # Get the image data
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # Display the image on the QLabel
            img_label.setPixmap(pixmap.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # self.image_away_team.setPixmap(pixmap.scaled(self.image_away_team.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            print("Failed to download image:", reply.errorString())

        # Cleanup
        reply.deleteLater()

# Main part to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SimpleForm()
    window.show()

    sys.exit(app.exec_())