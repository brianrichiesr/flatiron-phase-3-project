#!/usr/bin/env python
from clear_screen import clear
from games.wordle.wordle import start_wordle
from games.minesweeper.minesweeper import start_minesweeper
from gamestats.stats import show_stats
from games.hangman.hangman import start_hangman
from games.anagrams.anagrams import start_anagrams
from games.typeracer.typeracer import start_typeracer
from games.wordle.player import Player
from database.orm import Database
import time

# Print the menu of options when the user starts up the app
def main():
    user = None
    user_name = input("Please enter a username between 1-10 letters: ")
    try:
        if(Database.insert_player(user_name)):
                user = Player(user_name)
        else:
            print("Player with that username was found, logging in...")
            time.sleep(1)
            user = Player(user_name)
    except Exception as e:
        print(e)
    while True:
        clear()
        print("1. Play Wordle")
        print("2. Play Minesweeper")
        print("3. Play Hangman")
        print("4. Play Anagrams")
        print("5. Play Typeracer")
        print("17. View Stats")
        print("18. Exit program")
        choice = input("> ")
        if choice == "1":
            start_wordle(user)
        elif choice == "2":
            start_minesweeper(user)
        elif choice == "3":
            start_hangman(user)
        elif choice == "4":
            start_anagrams(user)
        elif choice == "5":
            start_typeracer(user)
        elif choice == "17":
            show_stats(user)
        elif choice == "18":
            exit()
        else:
            print("Invalid choice")

# If this file is ran as the main and not imported it will run main()
if __name__ == "__main__":
    main()