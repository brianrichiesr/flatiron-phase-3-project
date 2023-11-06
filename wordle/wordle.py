#!/usr/bin/env python
# Import classes/data/modules
from .game import Game
from .player import Player
from .solution import Solution
from wordle.colors import *
from .valid_words import valid_words
import curses
import time

# Function that asks for user name when is_playing is False and
#   shows the game when is_playing is True
def start_wordle():
    is_playing = False
    user = None
    user_name = input("Please enter a username between 1-10 letters: ")
    try:
        user = Player(user_name)
        is_playing = True
    except Exception as e:
        print(e)
    curses.wrapper(lambda x: wordle(x, user, is_playing))


#!main game loop:
def wordle(stdscr, user, is_playing):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Set up the screen
    new_game = Game(user)
    # curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    user_guess = ""
    idx = 0

    # Function that will iterate through all the user's guess in current game
    #   and print them on the screen with the correct colors
    def print_all_guesses():
        stdscr.clear()
        for guess in new_game.guesses:
            print_colored_word(stdscr,guess,new_game.solution.solution)
            stdscr.addch('\n')

    # During while loop iteration, which will constantly run while is_playing
    #   is True, allow user to play game
    while is_playing:
        # Store value of the key user pressed in demo
        key = stdscr.getch()
        # If keyboard key is pressed
        if key != -1:
            # If key is delete or backspace
            if key == 127 or key == 263:
                # Remove last character from user_guess
                user_guess = user_guess[:-1]

            # If user_guess length is less than 5
            elif len(user_guess) < 5 and chr(key).isalpha():  
                # Add current key value in uppercase to user_guess
                user_guess += chr(key).upper()
                
            # If the key pressed was return or enter
            if key == 10:
                # If the length of user_guess is 5
                if len(user_guess) == 5:
                    # If evaluation of user_guess in the new_game.guess method
                    #   returns True, user wins
                    if new_game.guess(user_guess):
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'You won! The word was {user_guess}')
                        stdscr.refresh()
                        time.sleep(3.0)
                        user_guess = ""
                        is_playing = False
                        stdscr.clear()
                    else:
                        # If the user_guess is included in the valid_words data, print
                        #   all guesses
                        if user_guess.lower() in valid_words:
                            print_all_guesses()
                            stdscr.refresh()
                            idx = len(new_game.guesses)
                            user_guess=""
                            # If there has been a total of 6 guesses, user loses
                            if idx == 6:
                                stdscr.clear()
                                stdscr.addstr(0, 0, f"Game over. {new_game.solution.solution}")
                                stdscr.refresh()
                                time.sleep(3.0)
                                is_playing = False
                                stdscr.clear()
                                break
                        else:
                            stdscr.clear()
                            stdscr.addstr(0, 0, "Enter a valid 5-letter word.")
                            stdscr.refresh()
                            time.sleep(1.0)
                            print_all_guesses()
                            # all=""
                            stdscr.addstr(user_guess)
                            stdscr.refresh()

            else:
                stdscr.deleteln()
                stdscr.move(idx,0)
                stdscr.addstr(user_guess)
                stdscr.refresh()

        if key == 27:
            break
    
    
