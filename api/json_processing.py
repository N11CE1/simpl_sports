import json


def find_items(data, target_key):
    """
    Recursively find all the lists associated with the given key, and return the individual items as dictionaries.
    :param data: The JSON data (dictionary or list)
    :param target_key: The key to search for
    :return: A list of dictionaries where each dictionary is an individual item in the "items" list
    """
    items = []

    if isinstance(data, dict):
        # If the data is a dictionary, check if the key exists
        for key, value in data.items():
            if key == target_key and isinstance(value, list):
                # If the key is found and the value is a list, iterate through the list and add to items
                for item in value:
                    if isinstance(item, dict):
                        items.append(item)  # Add each item as a separate dictionary
            # Recur for the value if it's a dictionary or list
            elif isinstance(value, (dict, list)):
                items.extend(find_items(value, target_key))

    elif isinstance(data, list):
        # If the data is a list, iterate over each element
        for item in data:
            items.extend(find_items(item, target_key))

    return items

# Load the JSON file
with open(r'unit test json\nhl_standings.json', 'r') as file:
    json_data = json.load(file)

# Find and extract all items under the 'items' key
target_key = 'teams'
items = find_items(json_data, target_key)
teams = {}
# Print the individual items (each item is now a dictionary)
x = 0
for item in items:
    teams[x] = item
    x += 1

for key, team in teams.items():
    print(team)
    # print(f"id: {team['id']}" if 'id' in team else None)
    # print(f"market: {team['market']}" if 'market' in team else None)
    # print(f"name: {team['name']}" if 'name' in team else None)
    # print(f"wins: {team['wins']}" if 'wins' in team else 0)
    # print(f"losses: {team['losses']}" if 'losses' in team else 0)
    # print(f"win_pct: {team['win_pct']}" if 'win_pct' in team else 0)
    # print(f"points_for: {team['points_for']}" if 'points_for' in team else 0)
    # print(f"points_against: {team['points_against']}" if 'points_against' in team else 0)
    # print(f"point_diff: {team['point_diff']}" if 'point_diff' in team else 0)
    # "name": team['market'] if 'market' in team else "" + team['name'] if 'name' in team else "",
    # "wins": team['wins'] if 'wins' in team else 0,
    # "losses": team['losses'] if 'losses' in team else 0,
    # "win_pct": team['win_pct'] if 'win_pct' in team else 0,
    # "points_for": team['points_for'] if 'points_for' in team else 0,
    # "points_against": team['points_against'] if 'points_against' in team else 0,
    # "point_diff": team['point_diff'] if 'point_diff' in team else 0
    break