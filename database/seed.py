import sqlite3
import sys
import random
sys.path.append('.')
from wordle.valid_words import valid_words
from wordle.all_words import all_words
connection = sqlite3.connect("database/database.db")
cursor = connection.cursor()

    
#2 layers of security for deleting just in case
def seed(delete=None,extra=None):
    #! Delete tables if they exist, recreate them for fresh data
    with connection:
        if delete and extra == "Yes":
            tables = ['players','words','valid_words','games_played']
            for table in tables:
                cursor.execute(f'''DROP TABLE IF EXISTS {table}''')
                connection.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT UNIQUE NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valid_words (
            id INTEGER PRIMARY KEY,
            word TEXT UNIQUE NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games_played (
            id INTEGER PRIMARY KEY,
            game_name TEXT NOT NULL,
            time_played FLOAT NOT NULL,
            win INTEGER NOT NULL,
            score FLOAT NOT NULL,
            player_id INTEGER NOT NULL
            );
        ''')

    #!Seeding test for players
    names = ["Peter", "Ronald", "Blake", "Andrew", "Sienna", "Charlie", "Jason", "Samantha", "John", "Hamburglar"]
    with connection:
        for name in names:
            cursor.execute('''
                INSERT INTO players (name) VALUES (?);
            ''', (name,))

        result = cursor.execute("SELECT * FROM players").fetchall()
        for res in result:
            print(f'Player {res[1]} populated with id: {res[0]}')
        connection.commit()
    

    #!Seeding test for all possible wordle guesses
    words = valid_words

    with connection:
        for word in words:
            cursor.execute("INSERT OR IGNORE INTO words (word) VALUES (?)",(word,))

    result = cursor.execute("SELECT * FROM words").fetchall()
    connection.commit()
    print(f"Populated valid words, len: {len(result)}")


    #!Seeding test for all possible wordle solutions (Easier to guess than all possible words)
    words = all_words

    with connection:
        for word in words:
            cursor.execute("INSERT OR IGNORE INTO valid_words (word) VALUES (?)",(word,))

    result = cursor.execute("SELECT * FROM valid_words").fetchall()
    connection.commit()
    print(f"Populated solutions, len: {len(result)}")


    #!Seeding test for random games played
    with connection:
        fake_data = [
        ("Chess", random.uniform(0.5, 5.0), random.choice([0, 1]), random.uniform(0.0, 100.0), random.randint(1, 10)),
        ("Checkers", random.uniform(0.5, 5.0), random.choice([0, 1]), random.uniform(0.0, 100.0), random.randint(1, 10)),
        ("Monopoly", random.uniform(0.5, 5.0), random.choice([0, 1]), random.uniform(0.0, 100.0), random.randint(1, 10)),
        ]
        for entry in fake_data:
            cursor.execute('''
                INSERT INTO games_played (game_name,time_played,win,score,player_id) VALUES (?,?,?,?,?)
            ''',entry)
        
        result = cursor.execute("SELECT * FROM games_played").fetchall()
        print(f'All games played: {result}')

seed(True,"Yes")
# seed()


