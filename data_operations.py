import sqlite3
import pandas as pd

pd.set_option('display.max_colwidth', None)

# Initiate Connection to Database
def connect_to_database():
    """Connect to the SQLite database. If the database does not exist, it will be created."""
    try:
        # Connect to the SQLite database (if it does not exist, it will be created)
        connection = sqlite3.connect('simpl_sports.db')
        return connection
    except sqlite3.Error as e:
        print(f"Error while connecting to the database: {e}")
        return None


# Save Data to Database
def save_sports_info(sport_data): # sports_id, name, description
    conn = connect_to_database()
    cursor = conn.cursor()

    try:

        columns = ', '.join(sport_data.columns)
        placeholders = ', '.join(['?'] * len(sport_data.columns))  # For prepared statement placeholders
        insert_sql = f"INSERT INTO tbl_sport ({columns}) VALUES ({placeholders})"

        # Convert DataFrame to a list of tuples for executemany
        data_to_insert = [tuple(row) for row in sport_data.values]

        # Use executemany to insert all rows efficiently
        cursor.executemany(insert_sql, data_to_insert)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        # Close the connection
        conn.close()

def save_league_info(league_data): # league_id, name, short_name, logo (optional)
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        columns = ', '.join(league_data.columns)
        placeholders = ', '.join(['?'] * len(league_data.columns))  # For prepared statement placeholders
        insert_sql = f"INSERT INTO tbl_leagues ({columns}) VALUES ({placeholders})"

        data_to_insert = [tuple(row) for row in league_data.values]

        cursor.executemany(insert_sql, data_to_insert)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

def save_team_info(team_data, league_id): # team_id (system), shortname, name, badge (optional)
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # delete existing records first
        delete_query = f"DELETE FROM tbl_teams WHERE sportsdb_id = ?"
        cursor.execute(delete_query, (league_id,))

        # replace the deleted records with new records
        columns = ', '.join(team_data.columns)
        placeholders = ', '.join(['?'] * len(team_data.columns))  # For prepared statement placeholders
        insert_sql = f"INSERT INTO tbl_teams ({columns}) VALUES ({placeholders})"
        data_to_insert = [tuple(row) for row in team_data.values]
        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()

        # delete this!
        print("Teams info saved to database.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

# Update Data on Database
def update_sports_info(column_values):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        set_clause = ', '.join([f"{col} = ?" for col in column_values.keys()])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

def update_league_info():
    pass
def update_team_info():
    pass

# Retrieve Data from Database
def get_sports_info(sport_id):
    conn = connect_to_database()
    query = "SELECT * FROM tbl_sports WHERE sport_id = ?"
    df = pd.read_sql_query(query, conn, params=(sport_id,))
    if conn:
        conn.close()

    return df

def get_leagues():
    conn = connect_to_database()
    query = "SELECT * FROM tbl_leagues"
    df = pd.read_sql_query(query, conn)
    if conn:
        conn.close()

    return df

def get_league_info(league_id):
    conn = connect_to_database()
    query = "SELECT * FROM tbl_leagues WHERE league_id = ?"
    df = pd.read_sql_query(query, conn, params=(league_id,))
    if conn:
        conn.close()

    return df

def get_team_info(team_id):
    conn = connect_to_database()
    query = "SELECT * FROM tbl_teams WHERE team_id = ?"
    df = pd.read_sql_query(query, conn, params=(team_id,))
    if conn:
        conn.close()

    return df

def get_league_badge(league_id):
    conn = connect_to_database()
    query = "SELECT badge FROM tbl_leagues WHERE league_id = ?"
    df = pd.read_sql_query(query, conn, params=(league_id,))
    result_string = df['badge'].to_string(index=False, header=False)
    if conn:
        conn.close()

    return result_string

def get_team_badge(team_id):
    pd.set_option('display.max_colwidth', None)
    conn = connect_to_database()
    query = "SELECT badge FROM tbl_teams WHERE team_id = ?"
    df = pd.read_sql_query(query, conn, params=(team_id,))
    result_string = df['badge'].to_string(index=False, header=False)
    if conn:
        conn.close()

    return result_string
