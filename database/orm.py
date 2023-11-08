import sqlite3
import random
connection = sqlite3.connect("database/database.db")
cursor = connection.cursor()

class Database:

    #Get all player objects from db
    @classmethod
    def get_all_players(cls):
        with connection:
            return cursor.execute("SELECT * FROM players").fetchall()
    
    #Get single player object from db
    @classmethod
    def get_player(cls,name):
        with connection:
            return cursor.execute("SELECT * FROM players WHERE name = ? COLLATE NOCASE",(name,)).fetchone()
    
    #Get list of players played games from db
    @classmethod
    def get_player_games(cls,name):
        with connection:
            return cursor.execute("SELECT games_played.* FROM players JOIN games_played ON players.id = games_played.player_id WHERE name = ? COLLATE NOCASE ORDER BY games_played.game_name",(name,)).fetchall()

    #Checks if given word is a valid wordle guess against db words
    @classmethod
    def is_valid_word(cls,word):
        with connection:
            return cursor.execute("SELECT * FROM words WHERE word = ? COLLATE NOCASE",(word,)).fetchone()
        
    #Gets a random wordle solution word from db
    @classmethod
    def get_random_word(cls):
        all_words = cursor.execute("SELECT * FROM valid_words").fetchall()
        return all_words[random.randint(0,len(all_words))]
    
    #Gets random hangman solution from db
    @classmethod
    def get_random_hangman_word(cls):
        all_words = cursor.execute("SELECT * FROM hangman_words").fetchall()
        return all_words[random.randint(0,len(all_words))]
    
    #Inserts player object into db
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
    
    #Inserts a game record into db
    @classmethod
    def insert_game(cls,game_tuple):
         #!Game tuple should be a tuple with arguments (game_name,time_played,player_id)
         with connection:
            cursor.execute("INSERT INTO games_played (game_name,time_played,win,score,player_id) VALUES (?,?,?,?,?)",game_tuple)
            connection.commit()

    
    #Gets a players highest score game from db
    @classmethod
    def best_game(cls,name):
            return cursor.execute('''
            SELECT games.game_name, games.time_played, games.win, MAX(games.score) AS max_score
            FROM players
            JOIN games_played AS games ON players.id = games.player_id
            WHERE players.name = ? COLLATE NOCASE
            GROUP BY players.name, games.game_name
            ORDER BY max_score DESC
            LIMIT 1;
        ''',(name,)).fetchone()


#!TODO
#CLASSMETHODS
#Get all players
#Get specific player
#Get all played games from player
#Get random word
#Check for valid word
#Insert player
#Insert game played

# print(Database.get_all_players())
# print(Database.get_player("samantha"))
# print(Database.get_player_games("peter"))
# print(Database.get_random_word())
# print(Database.insert_player("samanth"))
# print(Database.is_valid_word("tests"))
# print(Database.best_game("danner"))