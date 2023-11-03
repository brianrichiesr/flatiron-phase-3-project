#!/usr/bin/env python
from classes.game import Game
from classes.player import Player
from classes.solution import Solution
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
    # Set up the screen
    new_game = Game(user)
    print(new_game.solution)
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    all = ""

    while is_playing:
        key = stdscr.getch()
        
        if key != -1:
            if key == 127:
                all = all[:-1]

            elif len(all) < 5 and chr(key).isalpha():  
                all += chr(key)
            
            if key == 10:
                if len(all) == 5:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f'You chose: {all}')
                    stdscr.refresh()
                    if new_game.guess(all):
                        all = ""
                        stdscr.clear()
                        stdscr.addstr(0, 0, f'You won! The word was {all}')
                        stdscr.refresh()
                    else:
                        stdscr.clear()
                        for idx,guess in enumerate(new_game.guesses):
                            stdscr.addstr(idx, 0, f'{guess}')
                        stdscr.refresh()
                        all = ""
                    
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f'Current word: {all}')
                stdscr.refresh()


        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
