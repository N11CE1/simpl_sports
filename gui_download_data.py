import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import api_handler as api
import pandas as pd
import api_constants as ac

class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        layout = QVBoxLayout(self)

        teams = api.get_teams_in_league(ac.sportsdb_leagues[3])
        # print(teams)
        df = pd.json_normalize(teams, 'teams', sep='_')
        print(df[['strTeamShort', 'strTeam', 'strSport', 'strBadge']])

        # # Create a QTableView
        # self.table_view = QTableView(self)
        #
        # # Create a QStandardItemModel to hold the data
        # model = QStandardItemModel(5, 4)  # 5 rows, 3 columns
        # model.setHorizontalHeaderLabels(['Sport', 'Short Team Name', 'Team Name', 'Image URL'])  # Set column headers

        # Add some sample data to the model
        # data = [
        #     ["Alice", "25", "New York"],
        #     ["Bob", "30", "Los Angeles"],
        #     ["Charlie", "35", "Chicago"],
        #     ["David", "40", "San Francisco"],
        #     ["Eve", "22", "Austin"]
        # ]

        # # Populate the model with data
        # for row in range(5):
        #     for col in range(3):
        #         item = QStandardItem(data[row][col])
        #         model.setItem(row, col, item)

        # Set the model on the QTableView
        # self.table_view.setModel(model)

        # Add the QTableView to the layout
        # layout.addWidget(self.table_view)

        # Set up the window
        self.setWindowTitle("Updated Database...")
        self.setGeometry(100, 100, 400, 300)

# Main part to run the application
def main():
    # Create the application object
    app = QApplication(sys.argv)

    # Create the form (main window)
    form = Downloader()

    # Show the form
    form.show()

    app.exec_()

    # Execute the application's event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    # to do: open form first before downloading image