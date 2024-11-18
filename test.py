import shared

class TestClass:
    def __init__(self, sports_order):
        self.sports_order = sports_order


test = TestClass({0: "nba", 1: "nfl", 2: "nhl", 3: "epl"})

for sports in test.sports_order.values():
    print(sports)