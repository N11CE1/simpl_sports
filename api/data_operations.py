import sqlite3
import pandas as pd
from PyQt5.QtGui import QPixmap, QImage
from api import api_handler as ah
pd.set_option('display.max_colwidth', None)

# Initiate Connection to Database
def connect_to_database():
    """Connect to the SQLite database. If the database does not exist, it will be created."""
    try:
        connection = sqlite3.connect('simpl_sports.db')
        return connection
    except sqlite3.Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

def initialize_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('''
         CREATE TABLE IF NOT EXISTS tbl_leagues (
             short_name TEXT,
             name TEXT,
             badge_url TEXT,
             badge_image BLOB,
             sportsdb_id TEXT
         )
         ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_teams (
                            "team_id"	INTEGER,
                            "short_name"	TEXT,
                            "name"	TEXT,
                            "badge"	TEXT,
                            "sport"	TEXT,
                            "sportsdb_id"	TEXT,
                            "image"	BLOB,
                            PRIMARY KEY("team_id" AUTOINCREMENT)
        )
                ''')

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

def save_league_info(league_data):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        delete_query = f"DELETE FROM tbl_leagues"
        cursor.execute(delete_query)

        query = "INSERT INTO tbl_leagues VALUES(?, ?, ?, ?, ?)"
        cursor.executemany(query, league_data)
        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

def save_team_info(team_data, league_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:

        delete_query = f"DELETE FROM tbl_teams WHERE sportsdb_id = ?"
        cursor.execute(delete_query, (league_id,))

        columns = ', '.join(team_data.columns)
        placeholders = ', '.join(['?'] * len(team_data.columns))
        insert_sql = f"INSERT INTO tbl_teams ({columns}) VALUES ({placeholders})"
        data_to_insert = [tuple(row) for row in team_data.values]
        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()

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

def get_league_teams(sportsdb_id):
    conn = connect_to_database()
    query = "SELECT short_name, name, sport, sportsdb_id FROM tbl_teams WHERE sportsdb_id = ?"
    df = pd.read_sql_query(query, conn, params=(sportsdb_id,))
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

def get_team_info(short_name=None, name=None, sportsdb_id=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    if name is None:
        query = "SELECT * FROM tbl_teams WHERE short_name = ? AND sportsdb_id = ?"
        df = pd.read_sql_query(query, conn, params=(short_name, sportsdb_id,))
    else:
        stmt = '%' + name + '%'
        query = "SELECT * FROM tbl_teams WHERE name LIKE ? AND sportsdb_id = ?"
        df = pd.read_sql_query(query, conn, params=(stmt, sportsdb_id,))
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

def get_team_image(short_name=None, name=None, sportsdb_id=None):
    conn = connect_to_database()
    cursor = conn.cursor()

    if name is None:
        query = "SELECT image FROM tbl_teams WHERE short_name = ? AND sportsdb_id = ?"
        cursor.execute(query, (short_name, sportsdb_id))
    else:
        query = "SELECT image FROM tbl_teams WHERE name = ? AND sportsdb_id = ?"
        cursor.execute(query, (name, sportsdb_id))

    image_data = cursor.fetchone()
    pmap = QPixmap()

    try:
        if image_data:
            # Convert the BLOB data to QImage
            image_bytes = image_data[0]
            image = QImage.fromData(image_bytes)

            if image.isNull():
                print("Failed to load image from database.")
            else:
                pmap = QPixmap.fromImage(image)
        else:
            print("No image found in the database.")
    except sqlite3.Error as e:
        print(f"Error loading image from database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        conn.close()

    return pmap

def get_team_logo(url):
    image_data = ah.get_sportsdb_team_image(url)
    return image_data

def save_image_to_db(image_data, name, sportsdb_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    if image_data is not None:
        try:
            query = f"""
                        UPDATE tbl_teams
                        SET image = ?
                        WHERE name = ? AND sportsdb_id = ?
                    """

            cursor.execute(query, (image_data.getvalue(), name, sportsdb_id))

            conn.commit()

        except sqlite3.Error as e:
            print(f"Saving: An error occurred: {e}")
        finally:
            conn.close()
