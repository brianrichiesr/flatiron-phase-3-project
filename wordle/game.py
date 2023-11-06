# Import classes/data
from .player import Player
from .solution import Solution
from .valid_words import valid_words

# Create Game class
class Game:
    # Class variable to store a record of all games each session
    all = []

    # Initialize class with player attribute, solution attribute made from
    #   imported Solution class, and a list of guesses attribute
    def __init__(self, player):
        self.player = player
        self.solution = Solution.create_solution()
        self.guesses = []
        type(self).all.append(self)
    
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
    
    # Function that checks if the users guess is in a list of valid words first,
    #   to ensure that the user is using actual words to play the game and not
    #   just some random letters to make solving the puzzle easier, then checks if 
    #   the user's guess is correct
    def guess(self, guess):
        if guess.lower() in valid_words:
            self.guesses.append(guess)
        return self.solution.solution == guess
    