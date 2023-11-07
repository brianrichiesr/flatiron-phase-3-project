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
        self.visible_board = self.create_board()
        self.hidden_board = self.create_board()
        type(self).all.append(self)
        self.set_mines()
        self.calculate_neighbor_numbers()

        self.tiles = set()

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
        else:
            self._rows = rows

    @property
    def cols(self):
        return self._cols
    
    @cols.setter
    def cols(self, cols):
        if not isinstance(cols, int):
            raise TypeError("Number of cols must be an integer")
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
        board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        return board
    
    def set_mines(self):
        mine_positions = set()
        while len(mine_positions) < self.mines:
            random_row = random.randint(0, self.rows - 1)
            random_col = random.randint(0, self.cols - 1)
            mine_positions.add((random_row, random_col))

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
                    for row in range(r - 1, r + 2):
                        for col in range(c - 1, c + 2):
                            if 0 <= row < self.rows and 0 <= col < self.cols and self.hidden_board[row][col] == 'B':
                                bomb_count += 1
                    if bomb_count > 0:
                        self.hidden_board[r][c] = str(bomb_count)

    def reveal_blanks(self, row, col):
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return
        if self.visible_board[row][col] != ' ':
            return 
        self.visible_board[row][col] = 'O'
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.hidden_board[r][c] == 'B':
                        continue
                    if self.hidden_board[r][c] == ' ':
                        self.reveal_blanks(r, c)
                    else:
                        self.visible_board[r][c] = self.hidden_board[r][c]
        
    
    def render(self):
        for row in range(self.rows + 2):
            for col in range((2 * self.cols) + 2):
                # TOP AND BOTTOM BORDERS
                if row == 0 or row == self.rows + 1:
                    self.stdscr.addch(row, col, '-')
                # SIDE BORDERS
                elif (col == 0 and (row != 0 or row != self.rows + 1)) or (col == (2 * self.cols) + 1 and (row != 0 or row != self.rows + 1)):
                    self.stdscr.addch(row, col, '|')
        for row in range(self.rows):
            for col in range(self.cols):
                # ADD BOARD
                self.stdscr.addch(row + 1, (2 * col) + 1, self.visible_board[row][col])
        self.stdscr.refresh()

    def handle_mouse_click(self, x, y):
        # is_playing = True
        if 0 <= x < 2 * self.cols and 0 <= y < self.rows + 1:
            col = x // 2
            self.tiles.add((y - 1, col))
            if self.hidden_board[y - 1][col] == 'B':
                # is_playing = False
                # pass
                self.visible_board[y - 1][col] = self.hidden_board[y - 1][col]
                self.stdscr.refresh()
            elif self.hidden_board[y - 1][col] == ' ':
                self.reveal_blanks(y - 1, col)
                self.stdscr.refresh()
            else:
                self.visible_board[y - 1][col] = self.hidden_board[y - 1][col]
                self.stdscr.refresh()
                

    