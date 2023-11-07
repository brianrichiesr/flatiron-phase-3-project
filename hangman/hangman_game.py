import sys
sys.path.append(".")
from wordle.player import Player
from wordle.solution import Solution
class HangmanGame:
    def __init__(self,player,solution):
        self.solution = solution
        self.player = player
    
    # Getter/Setter for player
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self, player):
        if not isinstance(player, Player):
            raise TypeError("Player must be a Player")
        else:
            self._player = player
    
    # Getter/Setter for solution 
    @property
    def solution(self):
        return self._solution
    
    @solution.setter
    def solution(self, solution):
        if not isinstance(solution, Solution):
            raise TypeError("Solution must be a Solution")
        else:
            self._solution = solution

    # @classmethod
    # def guess(guess):
        