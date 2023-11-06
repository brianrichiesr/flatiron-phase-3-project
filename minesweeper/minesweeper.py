# #!/usr/bin/env python
from .minesweeper_game import MinesweeperGame
from wordle.player import Player
import curses
# import time

def start_minesweeper():
    is_playing = False
    user = None
    user_name = input("Please enter a username between 1-10 letters: ")
    try:
        user = Player(user_name)
        is_playing = True
    except Exception as e:
        print(e)
    print("1. Beginner | 9 x 9 | 10 Mines")
    print("2. Intermediate | 16 x 16 | 40 Mines")
    print("3. Advanced | 30 x 16 | 99 Mines")
    difficulty = input("Please select a difficulty to start the game: ")
    curses.wrapper(lambda stdscr: minesweeper(stdscr, user, is_playing, difficulty))
    
def minesweeper(stdscr, user, is_playing, difficulty):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.refresh()
    if difficulty == "1":
        rows, cols, mines = 9, 9, 10
    elif difficulty == "2":
        rows, cols, mines = 16, 16, 40
    elif difficulty == "3":
        rows, cols, mines = 30, 16, 99
    else:
        print("Invalid choice")
        return None
    
    new_game = MinesweeperGame(user, rows, cols, mines)
    curses.mousemask(1)
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)

    while is_playing:
        try:
            new_game.render()
        except Exception as e:
            print(e)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            # new_game.handle_mouse_click(x, y)
        
