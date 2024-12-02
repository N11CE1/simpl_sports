import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class StatsChart(QWidget):
    def __init__(self, home_team, away_team, df_home, df_away, sport, parent=None):
        super().__init__(parent)
        self.home_team = home_team
        self.away_team = away_team
        self.df_home = df_home
        self.df_away = df_away
        self.sport = sport

        # Create the layout and canvas for the plot
        self.figure = plt.figure(figsize=(10, 6))
        self.canvas = FigureCanvas(plt.figure())

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Create the chart
        self.create_chart()

    def create_chart(self):
        print("Creating chart")
        try:
            # Prepare the data for plotting
            categories = ['Wins', 'Losses', 'Win %', 'Points For', 'Points Against', 'Point Diff']
            # home_stat_list = list(self.df_home.values())
            # Get the values for each statistic

            home_team_values = [
                self.df_home['wins'],
                self.df_home['losses'],
                self.df_home['win_pct'],
                self.df_home['points_for'],
                self.df_home['points_against'],
                self.df_home['point_diff']
            ]

            away_team_values = [
                self.df_away['wins'],
                self.df_away['losses'],
                self.df_away['win_pct'],
                self.df_away['points_for'],
                self.df_away['points_against'],
                self.df_away['point_diff']
            ]

            # Filter out categories where both teams have 0 values
            non_zero_categories = [i for i in range(len(categories)) if home_team_values[i] > 0 or away_team_values[i] > 0]
            filtered_categories = [categories[i] for i in non_zero_categories]
            filtered_home_team_values = [home_team_values[i] for i in non_zero_categories]
            filtered_away_team_values = [away_team_values[i] for i in non_zero_categories]

            # Set positions of bars on the x-axis for non-zero categories
            x = np.arange(len(filtered_categories))

            # Plotting the bar chart (side by side for each team)
            fig, ax = plt.subplots(figsize=(10, 6))

            # Bar chart for both teams side by side
            bar_width = 0.35  # Bar width for each team
            ax.bar(x - bar_width / 2, filtered_home_team_values, bar_width, label=self.home_team, color='b', edgecolor='black')
            ax.bar(x + bar_width / 2, filtered_away_team_values, bar_width, label=self.away_team, color='r', edgecolor='black')

            # Labels, title, and custom x-axis tick labels
            ax.set_xlabel('Statistics')
            ax.set_ylabel('Values')
            ax.set_title(f'Statistics Comparison: {self.home_team} vs {self.away_team}')
            ax.set_xticks(x)
            ax.set_xticklabels(filtered_categories)

            # Rotate x-axis labels to avoid overlap
            plt.xticks(rotation=45, ha='right')  # Rotate by 45 degrees

            # Adjust the layout for better spacing
            plt.tight_layout()  # Automatically adjust subplot parameters to give some padding

            # Display the legend
            ax.legend()

            # Draw the plot on the canvas
            self.canvas.figure = fig
            self.canvas.draw()

            # Close the figure to release memory
            plt.close(fig)  # Close the figure to free up resources

        # def center_window(self):
        #     # Get the geometry of the screen and the window
        #     screen_geometry = self.screen().geometry()
        #     window_geometry = self.geometry()
        #
        #     # Calculate the position of the window to center it
        #     x = (screen_geometry.width() - window_geometry.width()) // 2
        #     y = (screen_geometry.height() - window_geometry.height()) // 2
        #
        #     # Move the window to the calculated position
        #     self.move(x, y)
            print("Chart created successfully")
        except Exception as e:
            print(f"Error in create_chart: {e}")
