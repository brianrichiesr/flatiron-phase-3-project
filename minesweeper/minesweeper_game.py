from ..wordle.player import Player

class MinesweeperGame:
    all = []

    def __init__(self, player, rows, cols, mines):
        self.player = player
        self.rows = rows
        self.cols = cols
        self.mines = mines
        type(self).all.append(self)
    
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
    
    
    
    
    