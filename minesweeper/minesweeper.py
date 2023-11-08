# #!/usr/bin/env python
from .minesweeper_game import MinesweeperGame
from wordle.player import Player
from clear_screen import clear
from database.orm import Database
import curses
import time


def start_minesweeper(user):
    clear()
    print("1. Beginner | 9 x 9 | 10 Mines")
    print("2. Intermediate | 16 x 16 | 40 Mines")
    print("3. Advanced |16 x 30 | 99 Mines")
    difficulty = input("Please select a difficulty to start the game: ")
    curses.wrapper(lambda stdscr: minesweeper(stdscr, difficulty, user))
    
def minesweeper(stdscr, difficulty, user):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    start_time = time.time()
    stdscr.clear()
    stdscr.refresh()
    if difficulty == "1":
        rows, cols, mines = 9, 9, 10
    elif difficulty == "2":
        rows, cols, mines = 16, 16, 40
    elif difficulty == "3":
        rows, cols, mines = 16, 30, 99
    else:
        print("Invalid choice")
        return None
    
    first_row = -1
    first_col = -1
    new_game = MinesweeperGame(rows, cols, mines)
    curses.curs_set(0)  # Hide the cursor
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)

    while new_game.is_playing:
        try:
            new_game.render()
        except Exception as e:
            print(e)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            click = None
            if bstate & curses.BUTTON1_CLICKED:
                click = "left"
            elif bstate & curses.BUTTON3_CLICKED:
                click = "right"
            if first_row == -1 and first_col == -1 and curses.BUTTON1_CLICKED:
                first_row, first_col = (y - 1, x // 2)
                new_game.set_mines(first_row, first_col)
                new_game.first_click = False
                new_game.calculate_neighbor_numbers()
            new_game.handle_mouse_click(x, y, click)

        if new_game.is_playing == "lose":
            end_time = time.time()
            time_took = end_time - start_time
            score = 0
            Database.insert_game(("Minesweeper", round(time_took, 2), 0, score, Database.get_player(user.username)[0]))
            new_game.final_message(f"Game over. You clicked on a bomb.", time_took, score)
        elif new_game.is_playing == "win":
            end_time = time.time()
            score = round(((rows * cols) - mines) * (60 / time_took), 0)
            Database.insert_game(("Minesweeper", round(time_took, 2), 1, score, Database.get_player(user.username)[0]))
            new_game.final_message("You won! All cells have been revealed.", time_took, score)

    

