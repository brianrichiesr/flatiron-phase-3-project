#!/usr/bin/env python
from .game import Game
from .player import Player
from .solution import Solution
from wordle.colors import *
from database.orm import Database
import curses
import time

def start_wordle():
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
    curses.wrapper(lambda x: wordle(x, user, is_playing))


#!main game loop:
def wordle(stdscr, user, is_playing):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Set up the screen
    new_game = Game(user)
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    all = ""
    idx = 0

    def print_all_guesses():
        stdscr.clear()
        for guess in new_game.guesses:
            print_colored_word(stdscr,guess,new_game.solution.solution)
            stdscr.addch('\n')


    while is_playing:
        key = stdscr.getch()
        
        if key != -1:
            if key == 127 or key == 263:
                all = all[:-1]

            elif len(all) < 5 and chr(key).isalpha():  
                all += chr(key).upper()
                
            
            if key == 10:
                if len(all) == 5:
                    if new_game.guess(all):
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'You won! The word was {all}')
                        stdscr.refresh()
                        time.sleep(3.0)
                        all = ""
                        is_playing = False
                        stdscr.clear()
                    else:
                        if Database.is_valid_word(all):
                            print_all_guesses()
                            stdscr.refresh()
                            idx = len(new_game.guesses)
                            all=""
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
                            stdscr.addstr(all)
                            stdscr.refresh()

            else:
                stdscr.deleteln()
                stdscr.move(idx,0)
                stdscr.addstr(all)
                stdscr.refresh()

        if key == 27:
            break