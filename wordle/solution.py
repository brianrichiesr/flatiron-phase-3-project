from database.orm import Database

# Create Solution class
class Solution:
    
    # Initialize class with solution attribute
    def __init__(self, solution):
        self.solution = solution
    
    # Getter/Setter for solution
    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, solution):
        if isinstance(solution, str):
            self._solution = solution.upper()
        else:
            raise TypeError("Solution must be a string")
    
    # Function that retrieves and returns a random word from all_words
    @classmethod
    def create_solution(cls):
        return cls(Database.get_random_word()[1])