#!/usr/bin/env python
from classes.game import Game
from classes.player import Player
from classes.solution import Solution
from color_test import *
import curses
is_playing = False
user = None
user_name = input("Please enter a username between 1-10 letters: ")


try:
    user = Player(user_name)
    is_playing = True
except Exception as e:
    print(e)

#!main game loop:
def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Set up the screen
    new_game = Game(user)
    print(new_game.solution)
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    all = ""
    idx = 0

    while is_playing:
        key = stdscr.getch()
        
        if key != -1:
            if key == 127:
                all = all[:-1]

            elif len(all) < 5 and chr(key).isalpha():  
                all += chr(key).upper()
                
            
            if key == 10:
                if len(all) == 5:
                    if new_game.guess(all):
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'You won! The word was {all}')
                        stdscr.refresh()
                        all = ""
                    else:
                        stdscr.clear()
                        for guess in new_game.guesses:
                            print_colored_word(stdscr,guess,new_game.solution.solution)
                            stdscr.addch('\n')
                        idx = len(new_game.guesses)
                        all=""
            else:
                stdscr.deleteln()
                stdscr.move(idx,0)
                stdscr.addstr(all)
                stdscr.refresh()

        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
