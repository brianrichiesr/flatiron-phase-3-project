from wordle.player import Player
import curses
import random
import time

class MinesweeperGame:

    # Initialize class with number of rows, cols, and mines
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        # Create two boards: Visible for what the player sees
        # Hidden for the game solution (Mines and numbers)
        self.visible_board = self.create_board()
        self.hidden_board = self.create_board()
        # Sets is_playing status to playing upon instantiation
        self.is_playing = "playing"
        # Upon instantiation, first click is true until the first box is revealed
        self.first_click = True
        self.numbers_found = 0
        self.total_numbers = 0
        self.flags = 0

        # Initialize the curses window
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.stdscr.refresh()
    
    # Creates an array of blank spaces with length of rows with each index being an array with length of columns
    def create_board(self):
        board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        return board
    
    # Assigns random mines using a random row and column depending on difficulty
    def set_mines(self, first_row, first_col):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)
            # If it is user's first click, it does not assign a bomb to that spot in the grid
            if self.first_click and (random_row, random_col) == (first_row, first_col):
                continue
            mine_positions.add((random_row, random_col))

        # If first click is a bomb, the bomb is reassigned a new position
        if (first_row, first_col) in mine_positions:
            mine_positions.remove((first_row, first_col))
            while True:
                new_random_row = random.randint(0, self.rows - 1)
                new_random_col = random.randint(0, self.cols - 1)
                if (new_random_row, new_random_col) not in mine_positions:
                    mine_positions.add((new_random_row, new_random_col))
                    break

        # Assigns an empty space for the visible board and B for the hidden board for reference
        for (row, col) in mine_positions:
            self.visible_board[row][col] = ' '
            self.hidden_board[row][col] = 'B'

    def calculate_neighbor_numbers(self):
        # Each neighbor for reference
            # Top Left: row - 1, col - 1
            # Top Middle: row - 1, col
            # Top Right: row - 1, col + 1
            # Middle Left: row, col - 1
            # Middle Middle: row, col
            # Middle Right: row, col + 1
            # Bottom Left: row + 1, col - 1
            # Bottom Middle: row + 1, col
            # Bottom Right: row + 1, col + 1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.hidden_board[r][c] == ' ':
                    bomb_count = 0
                    # These two for loops iterate through the neighbors referenced above
                    for row in range(r - 1, r + 2):
                        for col in range(c - 1, c + 2):
                            if 0 <= row < self.rows and 0 <= col < self.cols and self.hidden_board[row][col] == 'B':
                                bomb_count += 1
                    # Assigns an integer to the hidden board for number of mines around
                    if bomb_count > 0:
                        self.hidden_board[r][c] = str(bomb_count)

    # When a blank is clicked, this function reveals all blanks and neighboring numbers using recursion
    def reveal_blanks(self, row, col):
        # Checks if row and col are within the board or returns None
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return
        # Double checks that the spot clicked is blank or returns None
        if self.visible_board[row][col] != ' ':
            return 
        # Sets blank space to O on visible board
        self.visible_board[row][col] = 'O'
        # Iterate through the position's neighbor using the same loop in calculate_neighbor_numbers
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.hidden_board[r][c] == 'B':
                        continue
                    # Recursion
                    if self.hidden_board[r][c] == ' ':
                        self.reveal_blanks(r, c)
                    else:
                        self.visible_board[r][c] = self.hidden_board[r][c]

    # Reveals all mines on the board when a mine is clicked
    def reveal_all_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.hidden_board[row][col] == 'B':
                    self.visible_board[row][col] = 'B'
    
    # Updates number of flags on the board
    def update_flags(self):
        self.flags = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.visible_board[row][col] == '?':
                    self.flags += 1

    # Checks win condition: If numbers revealed == total amount of numbers in hidden board, win
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.hidden_board[row][col].isdigit():
                    self.total_numbers += 1
                if self.visible_board[row][col].isdigit():
                    self.numbers_found += 1
        if self.total_numbers == self.numbers_found and self.total_numbers > 0:
            return True
        else:
            return False

    # Clears the screen and displays message, time, and score
    def final_message(self, message, time_took, score):
        self.stdscr.clear()
        # Display message
        self.stdscr.addstr(0, 0, f"{message}")
        # Display time_took
        self.stdscr.addstr(1, 0, f"Seconds elapsed: {time_took:.0f}")
        # Display score
        self.stdscr.addstr(2, 0, f"Score: {score:.0f}")
        self.stdscr.refresh()
        time.sleep(3.0)
        self.stdscr.clear()
        self.stdscr.refresh()
        self.is_playing = False
    
    # Renders the board when game is started
    def render(self):
        # Iterate through dimensions of the board and add a border
        for row in range(self.rows + 2):
            for col in range((2 * self.cols) + 2):
                # TOP AND BOTTOM BORDERS
                if row == 0 or row == self.rows + 1:
                    self.stdscr.addch(row, col, '-')
                # SIDE BORDERS
                elif (col == 0 and (row != 0 or row != self.rows + 1)) or (col == (2 * self.cols) + 1 and (row != 0 or row != self.rows + 1)):
                    self.stdscr.addch(row, col, '|')
        # Add playing board relative to the border
        for row in range(self.rows):
            for col in range(self.cols):
                # ADD BOARD
                self.stdscr.addch(row + 1, (2 * col) + 1, self.visible_board[row][col])
        self.stdscr.move(self.rows + 3, 0)
        self.stdscr.deleteln()
        # Display numbers of flags left
        self.stdscr.addstr(self.rows + 3, 0, f"Flags: {int(self.mines) - int(self.flags)}")
        self.stdscr.refresh()

    # Handles every mouse click during the game
    def handle_mouse_click(self, x, y, click):
        # Checks if cursor position is within board dimensions
        if 0 <= x < 2 * self.cols and 0 <= y < self.rows + 1:
            # Floor division for column index since each column on the board has a space in between
            col = x // 2
            # If type of click is right click, handle flags
            if click == "right":
                # If position is a blank space, change it to a flag
                if self.visible_board[y - 1][col] == ' ':
                    self.visible_board[y - 1][col] = '?'
                    self.update_flags()
                    self.render()
                # If position is a flag, change back to a blank space
                elif self.visible_board[y - 1][col] == '?':
                    self.visible_board[y - 1][col] = ' '
                    self.update_flags()
                    self.render()
            # If type of click is left click, handle game logic
            elif click == "left":
                # If position is a bomb, reveal all bombs and set new is_playing status to lose
                if self.hidden_board[y - 1][col] == 'B':
                    self.reveal_all_mines()
                    self.render()
                    self.is_playing = "lose"
                    time.sleep(2.0)
                # If position is a blank space, run recursion function
                elif self.hidden_board[y - 1][col] == ' ':
                    self.reveal_blanks(y - 1, col)
                    self.stdscr.refresh()
                # If position is a number, reveal the number
                # If win condition is met, set is_playing status to win
                else:
                    self.visible_board[y - 1][col] = self.hidden_board[y - 1][col]
                    if self.check_win():
                        self.is_playing = "win"
                    self.stdscr.refresh()
                

    