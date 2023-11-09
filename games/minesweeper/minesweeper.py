# #!/usr/bin/env python
from .minesweeper_game import MinesweeperGame
from clear_screen import clear
from database.orm import Database
import curses
import time

# Starts minesweeper game:
# First clears terminal, prints difficulty choices, and asks for input
def start_minesweeper(user):
    clear()
    print("1. Beginner | 9 x 9 | 10 Mines")
    print("2. Intermediate | 16 x 16 | 40 Mines")
    print("3. Advanced |16 x 30 | 99 Mines")
    difficulty = input("Please select a difficulty to start the game: ")
    # Runs our minesweeper game loop using curses package
    curses.wrapper(lambda stdscr: minesweeper(stdscr, difficulty, user))
    
# Minesweeper game loop
def minesweeper(stdscr, difficulty, user):
    # Starts clock for game
    start_time = time.time()
    # Clear terminal screen
    stdscr.clear()
    stdscr.refresh()
    # Sets number of rows, cols, and mines depending on difficulty
    if difficulty == "1":
        rows, cols, mines = 9, 9, 10
    elif difficulty == "2":
        rows, cols, mines = 16, 16, 40
    elif difficulty == "3":
        rows, cols, mines = 16, 30, 99
    else:
        print("Invalid choice")
        return None
    
    # Assigns first click
    first_row = -1
    first_col = -1
    new_game = MinesweeperGame(rows, cols, mines)
    curses.curs_set(0)  # Hide the cursor
    curses.mousemask(curses.ALL_MOUSE_EVENTS) # Accept mouse events
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)

    # Game loop
    while new_game.is_playing:
        # Try rendering board to terminal if new_game object is created
        try:
            new_game.render()
        except Exception as e:
            print(e)
        # Gets input from user
        if new_game.check_win():
            new_game.is_playing = "win"
        key = stdscr.getch()
        # Quit function
        if key == ord('q'):
            break
        # If user input is a mouse click
        elif key == curses.KEY_MOUSE:
            # Get mouse position
            _, x, y, _, bstate = curses.getmouse()
            click = None
            # Set type of click to left click
            if bstate & curses.BUTTON1_CLICKED:
                click = "left"
            # Set type of click to right click
            elif bstate & curses.BUTTON3_CLICKED:
                click = "right"
            # If it is user's first click, render mines and calculate neighboring numbers
            if first_row == -1 and first_col == -1 and curses.BUTTON1_CLICKED:
                first_row, first_col = (y - 1, x // 2)
                new_game.set_mines(first_row, first_col)
                new_game.first_click = False
                new_game.calculate_neighbor_numbers()
            # Handles mouse click in minesweeper_game.py
            new_game.handle_mouse_click(x, y, click)

        # Lose logic
        if new_game.is_playing == "lose":
            end_time = time.time()
            time_took = end_time - start_time
            score = 0
            # Add game information to database
            Database.insert_game(("Minesweeper", round(time_took, 2), 0, score, Database.get_player(user.username)[0]))
            new_game.final_message(f"Game over. You clicked on a bomb.", time_took, score)
        # Win logic
        elif new_game.is_playing == "win":
            end_time = time.time()
            time_took = end_time - start_time
            score = round(((rows * cols) - mines) * (60 / time_took), 0)
            # Add game information to database
            Database.insert_game(("Minesweeper", round(time_took, 2), 1, score, Database.get_player(user.username)[0]))
            new_game.final_message("You won! All cells have been revealed.", time_took, score)

    

