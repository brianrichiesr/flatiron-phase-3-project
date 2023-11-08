#!/usr/bin/env python
import requests
import time
from threading import Timer
from clear_screen import clear
from database.orm import Database
from random import randint
import math



# Print the menu of options when the user starts up the app
def start_anagrams(user):

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

    # Function that prints info for the user to play the game
    def enter_word():
        # Clears the terminal
        clear()
        # Joins all of the user's guesses from current game and assigns them to variable
        guess_list = ", ".join(user_guesses)
        # Joins all of the random letters from current game and assigns them to variable
        random_letters = ", ".join(letter_list)
        # Prints user's guesses in terminal
        print(f"Chosen Words: {guess_list}")
        # Prints random letters in terminal
        print(f"{random_letters}")
        # Prompts user to guess a word from random letters
        guess = input("Create a word from the letters above that you have not already made: ")
        return guess
    
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
        
        # Print score
        print(f"Your total score was {score}")
        # Add game to database
        Database.insert_game(("Anagrams",round(end_time - start_time,2),3,score,Database.get_player(user.username)[0]))
        # Pause to allow user to read final results of game before returning back to main menu
        time.sleep(3)

    # Game function
    def play_game():
        # Assigns result of enter_word function in lowercase and stripped of leading and trailing whitespace
        guess = enter_word().lower().strip()
        # Create a boolean
        checker = True
        # If the user's guess is not at least 2 letters long
        if len(guess) < 2:
            # Print message
            print("Your guess must be at least 2 letters long")
            # Change boolean to False
            checker = False
        else:
            # Iterate through user's guess
            for letter in guess:
                # If it comes across a letter that is not in the list of random letters
                if not letter in letter_list:
                    # Print message
                    print("Only make words from letters in list")
                    # Change boolean to False
                    checker = False
                    # Break loop
                    break
                # If the user tries to use a letter more times than it occurred in the list of random letters
                if guess.count(letter) > letter_list.count(letter):
                    # Print message
                    print("You can only use a letter once for each occurrence in list")
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
                    print("Nice!!")
                    # Add guess to guess_list
                    user_guesses.append(guess)
                else:
                    # Print message to let user know that the word has already been added to acceptable guesses
                    print("No repeats")
            else:
                # Let user know that the word does not exist in the api
                print("That is not a valid word")
        # Pause long enough for user to read results of guess
        time.sleep(.8)
        # Mark time
        end_time = time.time()
        # If the user has been playing for less than 1 minute continue playing
        if end_time - start_time < 60:
            play_game()
        else:
            end_game(end_time)
    
    play_game()