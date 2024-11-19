"""

POC for passing data from one form to another

"""
import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from functools import partial
import datasets as da
import gui_league_info_view as glev # open a new window

class SimpleForm(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title and dimensions of the window
        self.setWindowTitle("League View")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(1000, 800)

        # move the form to the center on start-up
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)

        # Create widgets

        # Header
        self.header = QLabel("Leagues")
        self.header.setFixedHeight(60)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet(
            """
            QLabel {
                border: 2px solid white;
                font-size: 36px;
                font-weight: bold;
            }
            """
        )

        # Images
        self.image1 = QLabel("image")
        self.image1.setFixedSize(300, 300)
        self.image1.setAlignment(Qt.AlignCenter)
        self.image1.setCursor(Qt.PointingHandCursor)
        self.image1.mousePressEvent = lambda event, lbl=self.image1: self.on_label_click(event, lbl)

        self.image2 = QLabel("image")
        self.image2.setFixedSize(300, 300)
        self.image2.setAlignment(Qt.AlignCenter)
        self.image2.setCursor(Qt.PointingHandCursor)
        self.image2.mousePressEvent = lambda event, lbl=self.image2: self.on_label_click(event, lbl)

        self.image3 = QLabel("image")
        self.image3.setFixedSize(300, 300)
        self.image3.setAlignment(Qt.AlignCenter)
        self.image3.setCursor(Qt.PointingHandCursor)
        self.image3.mousePressEvent = lambda event, lbl=self.image3: self.on_label_click(event, lbl)

        self.image4 = QLabel("image")
        self.image4.setFixedSize(300, 300)
        self.image4.setAlignment(Qt.AlignCenter)
        self.image4.setCursor(Qt.PointingHandCursor)
        self.image4.mousePressEvent = lambda event, lbl=self.image4: self.on_label_click(event, lbl)

        parent_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        images_layout = QGridLayout()

        header_layout.addWidget(self.header)

        # Set spacing between rows and columns
        images_layout.setHorizontalSpacing(0)  # Set horizontal spacing between columns
        images_layout.setVerticalSpacing(100)    # Set vertical spacing between rows

        # Set margin around the layout (padding from window edges)
        images_layout.setContentsMargins(50, 20, 50, 100)

        images_layout.addWidget(self.image1, 0, 0)
        images_layout.addWidget(self.image2, 0, 1)
        images_layout.addWidget(self.image3, 1, 0)
        images_layout.addWidget(self.image4, 1, 1)

        parent_layout.addLayout(header_layout)
        parent_layout.addLayout(images_layout)

        # get league info
        da.fill_leagues_dataset()

        self.setLayout(parent_layout)

        self.set_widgets_object_name(self, da.leagues)

    def set_widgets_object_name(self, layout, df): # to store the index
        # Find all QLabel widgets in the layout
        labels = layout.findChildren(QLabel)
        cnt = 0
        # Set objectName for each QLabel
        for idx, label in enumerate(labels):
            if "image" in label.text().lower():
                # label.setObjectName(str(df.at[cnt, 'league_id']))
                label.setObjectName(str(cnt))
                self.load_image_from_web(label, df.at[cnt, 'badge_url'])
                cnt += 1

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
        else:
            print("Failed to download image:", reply.errorString())

        # Cleanup
        reply.deleteLater()

    def on_label_click(self, event, label):
        self.secondary_widget = glev.LeagueInformationViewForm(label.objectName(), label.pixmap())
        self.secondary_widget.show()

    def save_image_to_database(self):
        pass

# Main part to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SimpleForm()
    window.show()

    sys.exit(app.exec_())