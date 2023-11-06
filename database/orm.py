import sqlite3
import random
connection = sqlite3.connect("database/database.db")
cursor = connection.cursor()

class Database:
    def __init__(self):
        # with connection:
        pass

    @classmethod
    def get_all_players(cls):
        with connection:
            return cursor.execute("SELECT * FROM players").fetchall()
    
    @classmethod
    def get_player(cls,name):
        with connection:
            return cursor.execute("SELECT * FROM players WHERE name = ? COLLATE NOCASE",(name,)).fetchone()
        
    @classmethod
    def get_player_games(cls,name):
        with connection:
            return cursor.execute("SELECT games_played.* FROM players JOIN games_played ON players.id = games_played.player_id WHERE name = ? COLLATE NOCASE",(name,)).fetchall()

    @classmethod
    def get_all_words(cls):
        with connection:
            return cursor.execute("SELECT * FROM words").fetchall()
        
    @classmethod
    def get_random_word(cls):
        return cls.get_all_words()[random.randint(0,len(cls.get_all_words()))]
    
    @classmethod
    def insert_player(cls,name):
        with connection:
            playerExists = cursor.execute("SELECT * FROM players WHERE name = ? COLLATE NOCASE",(name,)).fetchone()
            if not playerExists:
                cursor.execute("INSERT INTO players (name) VALUES(?)",(name,))
                connection.commit()
                return True
            else:
                return False
    @classmethod
    def insert_game(cls,game_tuple):
         #!Game tuple should be a tuple with arguments (game_name,time_played,player_id)
         with connection:
            cursor.execute("INSERT INTO games_played (game_name,time_played,player_id) VALUES (?,?,?)",game_tuple)
            connection.commit()

#!TODO
#CLASSMETHODS
#Get all players
#Get specific player
#Get all played games from player
#Get all words
#Get random word
#Insert player
#Insert game played

# print(Database.get_all_players())
# print(Database.get_player("samantha"))
# print(Database.get_player_games("peter"))
# print(Database.get_random_word())
print(Database.insert_player("samanth"))