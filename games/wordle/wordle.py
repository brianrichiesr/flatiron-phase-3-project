#!/usr/bin/env python
from .wordle_game import WordleGame
# from games.wordle.player import Player
import sys
sys.path.append(".")
from games.wordle.colors import *
from database.orm import Database
from clear_screen import clear
import curses
import time
import re

# Function that asks for user name when is_playing is False and
#   shows the game when is_playing is True
def start_wordle(user):
    curses.wrapper(lambda x: wordle(x, user, True))


#!main game loop:
def wordle(stdscr, user, is_playing):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    start_time = time.time()

    # Set up the screen
    new_game = WordleGame(user)
    # curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    user_guess = ""
    idx = 0
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0,0,"Type a word to start and press enter to guess")
    stdscr.refresh()
    # Function that will iterate through all the user's guess in current game
    #   and print them on the screen with the correct colors
    def print_all_guesses():
        stdscr.clear()
        for guess in new_game.guesses:
            print_colored_word(stdscr,guess,new_game.solution.solution)
            stdscr.addch('\n')

    regex = re.compile(r"[^a-zA-Z]")

    def alpha(string):
        if regex.search(string):
            return False
        return True
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
            elif len(user_guess) < 5 and alpha(chr(key)):  
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
                        end_time = time.time()
                        score = (1000 / (round(end_time - start_time,2))) * (7 - len(new_game.guesses) + 5)
                        stdscr.addstr(0, 0, f'You won! The word was {user_guess}, it took you {end_time - start_time:.2f} seconds!\n\nYour score was {score:.2f}!')
                        Database.insert_game(("Wordle", round(end_time-start_time,2), 1, round(score,2), Database.get_player(user.username)[0]))
                        stdscr.refresh()
                        time.sleep(3.0)
                        user_guess = ""
                        is_playing = False
                        stdscr.clear()
                    else:
                        if Database.is_valid_word(user_guess):
                            print_all_guesses()
                            stdscr.refresh()
                            idx = len(new_game.guesses)
                            user_guess=""
                            # If there has been a total of 6 guesses, user loses
                            if idx == 6:
                                stdscr.clear()
                                end_time = time.time()
                                score = (1000 / (round(end_time - start_time,2))) * (7 - len(new_game.guesses))
                                stdscr.addstr(0, 0, f"Game over. {new_game.solution.solution}, it took you {end_time - start_time:.2f} seconds!\n\nYour score was {score:.2f}!")
                                Database.insert_game(("Wordle", round(end_time-start_time,2), 0, round(score,2), Database.get_player(user.username)[0]))
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