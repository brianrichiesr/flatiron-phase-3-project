import sqlite3
import sys
from ..wordle.valid_words import valid_words
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
with connection:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY,
        word TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        name TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games_played (
        id INTEGER PRIMARY KEY,
        game_name TEXT,
        time_played FLOAT,
        player_id INTEGER
        );
    ''')

def seed():
    #!Seeding test for players
    names = ["Peter", "Ronald", "Blake", "Andrew", "Sienna", "Charlie", "Jason", "Samantha", "John", "Hamburglar"]
    with connection:
        for name in names:
            cursor.execute('''
                INSERT INTO players (name) VALUES (?);
            ''', (name,))

        result = cursor.execute("SELECT * FROM players").fetchall()
        for res in result:
            print(res)
        connection.commit()
    
    #!Seeding test for all wordle words
    words = valid_words
    with connection:
        for word in words:
            cursor.execute("INSERT INTO words (word) VALUES (?)",(word,))

    result = cursor.execute("SELECT * FROM words").fetchall()
    print(len(result))

seed()


