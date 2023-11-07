import curses
import random
import time
import sys
sys.path.append(".")
from wordle.player import Player
from database.orm import Database

# List of words to choose from
word_list = ["hangman", "python", "curses", "game", "coding", "challenge"]

# Function to choose a random word from the list
def choose_word():
    return random.choice(word_list)

# Function to draw the hangman figure
def draw_hangman(stdscr, attempts):
    hangman = [
        "   ____  ",
        "  |    | ",
        "  |    " + ("O" if attempts < 6 else " "),
        "  |   " + ("/|\\" if attempts < 5 else " "),
        "  |   " + ("/ \\" if attempts < 4 else " "),
        "  |      ",
        "_______  "
    ]

    #Get index and line so we can print on seperate line
    for i, line in enumerate(hangman):
        #30 away so hangman display shows up in middle
        stdscr.addstr(i, 30, line)

#Start game func
def start_hangman():
    is_playing = False
    user = None
    while not user:
        user_name = input("Please enter a username between 1-10 letters: ")
        try:
            if(Database.insert_player(user_name)):
                user = Player(user_name)
            else:
                print("Player with that username was found, logging in...")
                time.sleep(1)
                user = Player(user_name)
            is_playing = True
        except Exception as e:
            print(e)
    curses.wrapper(lambda x: hangman(x, user, is_playing))

# Function to initialize and run the game
def hangman(stdscr,user,is_playing):
    stdscr.clear()
    stdscr.refresh()

    #Get random word and uppercase for game
    word = choose_word().upper()
    #Initialize array full of underscores because word starts blank
    word_display = ["_" for _ in word]
    #Guessed letters in a set because they cant be repeated
    guessed_letters = set()
    #var for attempts
    attempts = 6

    #Main game loop
    while True:
        stdscr.clear()

        # Drwaw the hangman
        draw_hangman(stdscr, attempts)

        # Display the current state of the word
        word_display_str = " ".join(word_display)

        #Show word with underlines for letters we dhavent guessed yet
        stdscr.addstr(10, 0, "Word: " + word_display_str)

        stdscr.addstr(12, 0, "Guessed letters: " + ", ".join(guessed_letters))

        # Get user input
        stdscr.addstr(14, 0, "Guess a letter: ")
        stdscr.refresh()
        #Get user input
        user_input = stdscr.getch()

        letter = chr(user_input).upper()
        guessed_letters.add(letter)

        #If letter is in word
        if letter in word:
            for i, char in enumerate(word):
                #Loop through index of word to find matching letter, and update from underscore to letter that was guessed, eg _ to A
                if char == letter:
                    word_display[i] = letter
        else:
            #If wrong, attempts goes down by 1
            attempts -= 1

        # Check for a win
        if "_" not in word_display:
            stdscr.clear()
            stdscr.addstr(0, 0, "Congratulations! You guessed the word.")
            stdscr.refresh()
            break

        # Check for a loss
        if attempts == 0:
            stdscr.clear()
            stdscr.addstr(0, 0,f"You lost. The word was: {word}")
            stdscr.refresh()
            break

    stdscr.getch()
