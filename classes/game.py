from player import Player
from solution import Solution
demo = Solution.create_solution()
print(f"Game.py - {demo.solution}")
class Game:

    def __init__(self, player, solution):
        self.player = player
        self.solution = solution
    
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
    
    def guess(self, guess):
        return self.solution.solution == guess