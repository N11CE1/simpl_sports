from PyQt5.QtWidgets import QApplication
from graph.graph_team_record_analysis import StatsChart as StatsChart
import sys

app = QApplication(sys.argv)

# Sample data
home_team = "Home Team"
away_team = "Away Team"
df_home = {'wins': 10, 'losses': 5, 'win_pct': 0.6667, 'points_for': 1000, 'points_against': 900, 'point_diff': 100}
df_away = {'wins': 8, 'losses': 7, 'win_pct': 0.5333, 'points_for': 950, 'points_against': 930, 'point_diff': 20}
sport = "Basketball"

stats_chart = StatsChart(home_team, away_team, df_home, df_away, sport)
stats_chart.show()

sys.exit(app.exec_())