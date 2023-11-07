import curses
import random
import time
import sys
import re
from clear_screen import clear
sys.path.append(".")
from wordle.player import Player
from database.orm import Database

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
def start_hangman(user):
    clear()
    curses.wrapper(lambda x: hangman(x, user, True))

# Function to initialize and run the game
def hangman(stdscr,user,is_playing):
    #Clear screen
    stdscr.clear()
    stdscr.refresh()

    #init timer
    start_time = time.time()

    #Get random word and uppercase for game
    word = Database.get_random_hangman_word()[1].upper()
    #Initialize array full of underscores because word starts blank
    word_display = ["_" for _ in word]
    #Guessed letters in a set because they cant be repeated
    guessed_letters = set()
    #var for attempts
    attempts = 6

    #Main game loop
    while is_playing:
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
        regex = re.compile(r"[^a-zA-Z]")

        def alpha(string):
            if regex.search(string):
                return False
            return True
        
        if alpha(chr(user_input).upper()):
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
                final_score = max(100 - (6 - attempts) * 10, 0)
                end_time = time.time()
                stdscr.clear()
                stdscr.addstr(0, 0, "Congratulations! You guessed the word.")
                Database.insert_game(("Hangman",round(end_time - start_time,2),1,final_score,Database.get_player(user.username)[0]))
                stdscr.refresh()
                time.sleep(2)
                is_playing = False
                stdscr.clear()
                break

            # Check for a loss
            if attempts == 0:
                final_score = max(60 - (6 - attempts) * 10, 0)
                end_time = time.time()
                stdscr.clear()
                stdscr.addstr(0, 0,f"You lost. The word was: {word}")
                Database.insert_game(("Hangman",round(end_time - start_time,2),0,final_score,Database.get_player(user.username)[0]))
                stdscr.refresh()
                time.sleep(2)
                is_playing = False
                stdscr.clear()
                break

