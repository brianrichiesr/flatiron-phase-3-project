from all_words import all_words
import random

class Solution:

    # https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93
    # website where we got the wordle words from
    
    def __init__(self, solution):
        self.solution = solution
        
    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, solution):
        if isinstance(solution, str):
            self._solution = solution
        else:
            raise TypeError("Solution must be a string")
    
    @classmethod
    def create_solution(cls):
        return cls(all_words[random.randint(0, (len(all_words) - 1))])