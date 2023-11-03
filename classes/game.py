from .player import Player
from .solution import Solution
print(f"Game.py - {Solution.create_solution().solution}")
class Game:
    all = []

    def __init__(self, player):
        self.player = player
        self.solution = Solution.create_solution()
        self.guesses = []
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
    def solution(self):
        return self._solution
    
    @solution.setter
    def solution(self, solution):
        if not isinstance(solution, Solution):
            raise TypeError("Solution must be a Solution")
        else:
            self._solution = solution
            # print(demo.solution)
    
    def guess(self, guess):
        self.guesses.append(guess)
        return self.solution.solution == guess
    