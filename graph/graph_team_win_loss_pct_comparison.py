import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


# Define the PyQt window class
class TeamComparison(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBA Teams Comparison")

        # Create the main widget and layout
        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        # Example data for two teams
        team_data = [
            {"id": 1, "name": "Team A", "wins": 50, "losses": 32, "win_pct": 0.610},
            {"id": 2, "name": "Team B", "wins": 45, "losses": 37, "win_pct": 0.549},
        ]

        # Extract data
        names = [team['name'] for team in team_data]
        wins = [team['wins'] for team in team_data]
        losses = [team['losses'] for team in team_data]
        win_pct = [team['win_pct'] for team in team_data]

        # Create the Matplotlib figure
        fig, ax1 = plt.subplots(figsize=(8, 5))

        # Bar graph for wins and losses
        bar_width = 0.35  # Width of the bars
        index = range(len(team_data))  # X-axis positions
        ax1.bar(index, wins, bar_width, label="Wins", color='green', alpha=0.7)
        ax1.bar([i + bar_width for i in index], losses, bar_width, label="Losses", color='red', alpha=0.7)

        # Create a secondary axis for win percentage
        ax2 = ax1.twinx()
        ax2.plot(index, win_pct, label="Win Percentage", color='blue', marker='o', linestyle='-', linewidth=2)

        # Set the labels and title
        ax1.set_xlabel("Teams")
        ax1.set_ylabel("Wins and Losses")
        ax2.set_ylabel("Win Percentage")
        ax1.set_xticks([i + bar_width / 2 for i in index])
        ax1.set_xticklabels(names)

        ax1.set_title("Comparison of NBA Teams: Wins, Losses, and Win Percentage")

        # Add legends
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        # Embed the Matplotlib figure into the PyQt window
        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas)

        # Set the main widget
        self.setCentralWidget(self.main_widget)


# # Main function to run the PyQt application
# def main():
#     app = QApplication(sys.argv)
#     window = TeamComparison()
#     window.resize(800, 600)
#     window.show()
#     sys.exit(app.exec_())
#
#
# # Run the application
# if __name__ == '__main__':
#     main()
