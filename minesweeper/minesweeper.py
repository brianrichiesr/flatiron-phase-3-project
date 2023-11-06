#!/usr/bin/env python
from .minesweeper_game import MinesweeperGame
from ..wordle.player import Player
import curses
import time

def start_minesweeper():
    is_playing = False
    user = None
    user_name = input("Please enter a username between 1-10 letters: ")
    try:
        user = Player(user_name)
        is_playing = True
    except Exception as e:
        print(e)
    curses.wrapper(lambda x: minesweeper(x, user, is_playing))


#!main game loop:
def minesweeper(stdscr, user, is_playing):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Set up the screen
    print("1. Beginner | 9 x 9 | 10 Mines \n 2. Intermediate | 16 x 16 | 40 Mines \n 3. Advanced | 30 x 16 | 99 Mines \n")
    difficulty = input("Please select a difficulty to start the game: ")
    if difficulty == 1:
        rows = 9
        cols = 9
        mines = 10
        new_game = MinesweeperGame(user, rows, cols, mines)
    elif difficulty == 2:
        rows = 16
        cols = 16
        mines = 40
        new_game = MinesweeperGame(user, rows, cols, mines)
    else:
        rows = 30
        cols = 16
        mines = 99
        new_game = MinesweeperGame(user, rows, cols, mines)
    
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    all = ""
    idx = 0

    while is_playing:
        new_game.create_board()
        # key = stdscr.getch()
        
        # if key != -1:
        #     if key == 127 or key == 263:
        #         all = all[:-1]

        #     elif len(all) < 5 and chr(key).isalpha():  
        #         all += chr(key).upper()
                
            
        #     if key == 10:
        #         if len(all) == 5:
        #             if new_game.guess(all):
        #                 stdscr.clear()
        #                 stdscr.addstr(0, 0, f'You won! The word was {all}')
        #                 stdscr.refresh()
        #                 time.sleep(3.0)
        #                 all = ""
        #                 is_playing = False
        #                 stdscr.clear()
        #             else:
        #                 if all.lower() in valid_words:
        #                     print_all_guesses()
        #                     stdscr.refresh()
        #                     idx = len(new_game.guesses)
        #                     all=""
        #                     if idx == 6:
        #                         stdscr.clear()
        #                         stdscr.addstr(0, 0, f"Game over. {new_game.solution.solution}")
        #                         stdscr.refresh()
        #                         time.sleep(3.0)
        #                         is_playing = False
        #                         stdscr.clear()
        #                         break
        #                 else:
        #                     stdscr.clear()
        #                     stdscr.addstr(0, 0, "Enter a valid 5-letter word.")
        #                     stdscr.refresh()
        #                     time.sleep(1.0)
        #                     print_all_guesses()
        #                     # all=""
        #                     stdscr.addstr(all)
        #                     stdscr.refresh()

        #     else:
        #         stdscr.deleteln()
        #         stdscr.move(idx,0)
        #         stdscr.addstr(all)
        #         stdscr.refresh()

        # if key == 27:
        #     break
    
    
