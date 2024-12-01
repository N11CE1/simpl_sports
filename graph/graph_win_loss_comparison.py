import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class BarChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wins vs Losses - NBA Game Comparison")

        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        # Example data for two teams
        team_data = [
            {"name": "Team A", "wins": 50, "losses": 32},
            {"name": "Team B", "wins": 45, "losses": 37},
        ]

        # Create the Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 5))

        # Side-by-side bar chart
        bar_width = 0.35  # Width of the bars
        index = range(len(team_data))  # X-axis positions
        ax.bar(index, [team['wins'] for team in team_data], bar_width, label="Wins", color='green')
        ax.bar([i + bar_width for i in index], [team['losses'] for team in team_data], bar_width, label="Losses", color='red')

        ax.set_xlabel("Teams")
        ax.set_ylabel("Games Played")
        ax.set_title("Comparison of Wins and Losses for Two Teams")
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels([team['name'] for team in team_data])

        ax.legend()

        # Embed the Matplotlib figure into the PyQt window
        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas)

        self.setCentralWidget(self.main_widget)

# # Main function to run the PyQt application
# def main():
#     app = QApplication(sys.argv)
#     window = BarChartWindow()
#     window.resize(800, 600)
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     main()
