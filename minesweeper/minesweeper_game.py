from wordle.player import Player
import curses
import random

class MinesweeperGame:
    all = []

    def __init__(self, player, rows, cols, mines):
        self.player = player
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = self.create_board()
        type(self).all.append(self)
        self.set_mines()

        # Initialize the curses window
        self.stdscr = curses.initscr()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        self.stdscr.refresh()
    
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
        if not isinstance(player, Player):
            raise TypeError("Player must be a Player")
        else:
            self._player = player

    @property
    def rows(self):
        return self._rows
    
    @rows.setter
    def rows(self, rows):
        if not isinstance(rows, int):
            raise TypeError("Number of rows must be an integer")
        # elif not 8 <= rows <= 30:
        #     raise ValueError("Number of rows must be between 8 and 30, inclusive")
        else:
            self._rows = rows

    @property
    def cols(self):
        return self._cols
    
    @cols.setter
    def cols(self, cols):
        if not isinstance(cols, int):
            raise TypeError("Number of cols must be an integer")
        # elif not 8 <= cols <= 16:
        #     raise ValueError("Number of cols must be between 8 and 30, inclusive")
        else:
            self._cols = cols
    
    @property
    def mines(self):
        return self._mines
    
    @mines.setter
    def mines(self, mines):
        if not isinstance(mines, int):
            raise TypeError("Number of mines must be an integer")
        else:
            self._mines = mines

    def create_board(self):
        board = [['X' for _ in range(self.cols)] for _ in range(self.rows)]
        return board
    
    def set_mines(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)
            mine_positions.add((random_row, random_col))

        for (row, col) in mine_positions:
            self.board[row][col] = 'B'

    
    def render(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.stdscr.addch(row, 2 * col, self.board[row][col])
        self.stdscr.refresh()

    def handle_mouse_click(self, x, y):
        if 0 <= x < 2 * self.cols and 0 <= y < self.rows:
            col = x // 2
            if self.board[y][col] == 'X':
                self.board[y][col] = 'O'
                self.render()



    
    
    
    