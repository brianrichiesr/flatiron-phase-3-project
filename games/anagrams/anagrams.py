#!/usr/bin/env python
import requests
import time
import curses
import re
from clear_screen import clear
from random import randint
import math
import sys
sys.path.append(".")
from database.orm import Database

# Print the menu of options when the user starts up the app
def start_anagrams(user):
    curses.wrapper(lambda x: anagrams(x, user))

def anagrams(stdscr, user):
    # List to hold the user's guesses
    user_guesses = []
    # String of vowels and consonants
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    # Function that will create and return a list of random letters
    def create_list():
        # Empty list
        new_list = []
        # Random number between 5 and 15
        list_len = randint(5, 15)
        # Number that is 1/3 of the list_len rounded up
        v_len = math.ceil(list_len / 3)
        # Number that is the result of subtracting v_len from list_len
        c_len = list_len - v_len
        # Iterate v_len number of times
        for v in range(0, v_len):
            # On each loop, append a random vowel to new_list
            new_list.append(vowels[randint(0, (len(vowels) - 1))])
        # Iterate c_len number of times
        for c in range(0, c_len):
            # On each loop, append a random consonant to new_list
            new_list.append(consonants[randint(0, (len(consonants) - 1))])
        
        return new_list
    
    # Assign the return of the create_list function in a variable accessible all subsequent functionality
    letter_list = create_list()

    regex = re.compile(r"[^a-zA-Z]")

    def alpha(string):
        if regex.search(string):
            return False
        return True
    
    # Function that will make a GET request to a url to check if the user's guess is an actual word
    def check_word(word):
        result = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        return result
    
    # Marks time when game starts
    start_time = time.time()

    def end_game(end_time):
        # Calculate score
        score = 0
        # Iterate through guess_list
        for item in user_guesses:
            # 25 points for each letter
            score += (len(item) * 25)
            # Bonus points for words longer than 3 letters
            if len(item) > 3:
                bonus = len(item) - 3
                score += ((bonus * bonus) * 50)
        
        stdscr.clear()
        # Print score
        stdscr.addstr(0,0,f"Your total score was {score}")
        stdscr.refresh()
        # Add game to database
        Database.insert_game(("Anagrams",round(end_time - start_time,2),3,score,Database.get_player(user.username)[0]))
        # Pause to allow user to read final results of game before returning back to main menu
        time.sleep(3)
        stdscr.clear()

    # Game function
    is_playing = True
    guess = ""
    stdscr.nodelay(1)
    stdscr.clear()
    while is_playing:
        guess_list = ", ".join(user_guesses)
        # Joins all of the random letters from current game and assigns them to variable
        random_letters = ", ".join(letter_list)
        # Prints user's guesses in terminal
        
        stdscr.addstr(0,0,f"Chosen Words: {guess_list}")
        # Prints random letters in terminal
        stdscr.addstr(1,0,f"{random_letters}")
        stdscr.addstr(2,0,"Create a word from the letters above that you have not already made: \n")
        stdscr.addstr(3,0,f"{guess}")
        stdscr.refresh()

        end_time = time.time()
        if end_time - start_time > 60:
            
            end_game(end_time)
            curses.endwin()
            is_playing = False
            stdscr.clear()

        key = stdscr.getch()

        if key != -1:
            if key == 27:
                break
            if key == 127 or key == 263:
            # Remove last character from user_guess
                guess = guess[:-1]
                stdscr.deleteln()
                stdscr.addstr(3,0,f"{guess}")

            # If guess is less than or equal to length of list of letters
            elif len(guess) <= len(letter_list) and alpha(chr(key)):  
                # Add current key pressed lowercased to current guess
                guess += chr(key).lower()

            if key == 10:
                checker = True
                # If the user's guess is not at least 2 letters long
                if len(guess) < 2:
                    # Print message
                    stdscr.clear()
                    stdscr.addstr("Word must be longer than 2 letters")
                    stdscr.refresh()
                    time.sleep(1.5)
                    # Change boolean to False
                    checker = False
                else:
                    # Iterate through user's guess
                    for letter in guess:
                        # If it comes across a letter that is not in the list of random letters
                        if not letter in letter_list:
                            # Print message
                            stdscr.clear()
                            stdscr.addstr("You can only use letters in the list")
                            stdscr.refresh()
                            time.sleep(1.5)
                            # Change boolean to False
                            checker = False
                            # Break loop
                            break
                        # If the user tries to use a letter more times than it occurred in the list of random letters
                        if guess.count(letter) > letter_list.count(letter):
                            # Print message
                            stdscr.clear()
                            stdscr.addstr("You can only use a letter once for each occurrence in list")
                            stdscr.refresh()
                            time.sleep(1.5)
                            # Change boolean to False
                            checker = False
                            # Break loop
                            break
                # If boolean remains True
                if checker:
                    # Assign the result of check_word function
                    is_word = check_word(guess)
                    # If the status_code of what is returned is 200 then user's guess is a word in the api
                    if is_word.status_code == 200:
                        # If the word has not already been guessed
                        if not guess in user_guesses:
                            # Print message
                            stdscr.clear()
                            stdscr.addstr("Nice!!")
                            stdscr.refresh()
                            time.sleep(1.5)
                            # Add guess to guess_list
                            user_guesses.append(guess)
                            guess = ""
                        else:
                            # Print message to let user know that the word has already been added to acceptable guesses
                            stdscr.clear()
                            stdscr.addstr("No repeats!")
                            stdscr.refresh()
                            time.sleep(1)
                    else:
                        # Let user know that the word does not exist in the api
                        stdscr.clear()
                        stdscr.addstr("That is not a valid word!!")
                        stdscr.refresh()
                        time.sleep(1)
                        guess = ""
    
