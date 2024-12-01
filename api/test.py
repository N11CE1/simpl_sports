import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import time  # Used for simulating delays between tasks

class BackgroundWorker(QThread):
    update_signal = pyqtSignal(str)  # Signal to send progress back to the main thread

    def __init__(self):
        super().__init__()
        self.counter = 0
        self._running = True  # A flag to control the loop

    def run(self):
        """Perform the task with a delay between steps"""
        print("Background thread started...")  # Debugging print
        while self._running:  # Loop will run indefinitely until explicitly stopped
            time.sleep(1)  # Simulate some work (delay for 1 second)
            self.counter += 1
            print(f"Performing task step {self.counter}")  # Debugging print
            self.update_signal.emit(f"Step {self.counter}")  # Emit the progress update to the UI

        # This will not be reached unless the loop is stopped
        print("Task stopped!")  # Debugging print
        self.update_signal.emit("Task stopped!")  # Update UI with task stop

    def stop(self):
        """Stop the task gracefully"""
        print("Stopping background task...")  # Debugging print
        self._running = False  # Set the running flag to False to stop the loop
        self.quit()  # Ensure the thread exits gracefully


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Non-Blocking QThread Loop Example")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Waiting for task to finish...", self)
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("Start Background Task", self)
        self.start_button.clicked.connect(self.start_background_task)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Task", self)
        self.stop_button.clicked.connect(self.stop_background_task)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)

        self.worker = None

    def start_background_task(self):
        """Start the background task"""
        self.worker = BackgroundWorker()
        self.worker.update_signal.connect(self.update_status)  # Connect signal to update UI
        self.worker.start()  # Start the worker thread

        # Disable the start button and enable the stop button
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_background_task(self):
        """Stop the background task"""
        if self.worker:
            self.worker.stop()  # Request the worker to stop
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_status(self, message):
        """Update the label with the task progress"""
        self.label.setText(message)  # Update the UI with the message


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())  # Start the main event loop

if __name__ == "__main__":
    main()
