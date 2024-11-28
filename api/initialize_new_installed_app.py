import sys
import time

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressDialog, QApplication, QDialog, \
    QListView, QAbstractItemView, QProgressBar
from api import background_worker as bgw

class LoadingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initializing Simpl Sports")
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowSystemMenuHint)

        layout = QVBoxLayout()

        self.loading_text = QLabel(self)
        self.loading_text.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.loading_text.setText("Loading items...")
        self.loading_text.setStyleSheet("font-size: 20px;")

        self.listView = QListView(self)
        self.model = QStringListModel()
        self.model.setStringList([])

        self.listView.setModel(self.model)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 122)
        self.progressBar.setValue(0)

        layout.addWidget(self.loading_text)
        layout.addWidget(self.listView)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

        self.worker_thread = bgw.Initialize_App(self)
        self.worker_thread.running_task.connect(self.update_from_worker)

        self.start_task()

    def closeEvent(self, event):
        """Override closeEvent to clean up worker thread on application close."""
        if self.worker_thread is not None:
            if self.worker_thread.isRunning():
                print("Worker thread is running. Stopping it now...")
                self.worker_thread.quit()
        event.accept()

    def start_task(self):

        self.worker_thread.start()

    def update_from_worker(self, loading_text, item, progress):
        self.loading_text.setText(loading_text)

        current_list = self.model.stringList()
        current_list.append(item)
        self.model.setStringList(current_list)
        index = self.model.index(len(current_list) - 1)
        self.listView.scrollTo(index, QAbstractItemView.PositionAtBottom)

        if self.progressBar.value() <= self.progressBar.maximum():
            self.progressBar.setValue(progress)

        if loading_text == "Done":
            self.close()
