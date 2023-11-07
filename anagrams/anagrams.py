#!/usr/bin/env python
import requests
import time
from clear_screen import clear
from database.orm import Database
from random import randint
import math



# Print the menu of options when the user starts up the app
def start_anagrams(user):

    user_guesses = []
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    def create_list():
        new_list = []
        list_len = randint(5, 15)
        v_len = math.ceil(list_len / 3)
        c_len = list_len - v_len
        for v in range(0, v_len):
            new_list.append(vowels[randint(0, (len(vowels) - 1))])
        for c in range(0, c_len):
            new_list.append(consonants[randint(0, (len(consonants) - 1))])
        return new_list

    letter_list = create_list()

    def enter_word():
        clear()
        guess_list = ", ".join(user_guesses)
        choices = ", ".join(letter_list)
        print(f"Chosen Words: {guess_list}")
        print(f"{choices}")
        guess = input("Create a word from the letters above that you have not already made: ")
        return guess

    def check_word(word):
        result = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        return result
    
    start_time = time.time()

    def play_game():
        guess = enter_word().lower().strip()
        checker = True
        if len(guess) < 2:
            print("Your guess must be at least 2 letters long")
            checker = False
        else:
            for letter in guess:
                if not letter in letter_list:
                    print("Only make words from letters in list")
                    checker = False
                    break
                if guess.count(letter) > letter_list.count(letter):
                    print("You can only use a letter once for each occurrence in list")
                    checker = False
                    break
        if checker:
            is_word = check_word(guess)
            if is_word.status_code == 200:
                if not guess in user_guesses:
                    print("Nice!!")
                    user_guesses.append(guess)
                else:
                    print("No repeats")
            else:
                print("That is not a valid word")
        time.sleep(.8)
        end_time = time.time()
        if end_time - start_time < 60:
            play_game()
        else:
            score = 0
            for item in user_guesses:
                score += (len(item) * 25)

            print(f"Your total score was {score}")
            Database.insert_game(("Anagrams",round(end_time - start_time,2),3,score,Database.get_player(user.username)[0]))
            time.sleep(4)
    
    play_game()