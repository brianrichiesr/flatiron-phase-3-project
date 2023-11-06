#!/usr/bin/env python
from clear_screen import clear
from wordle.wordle import start_wordle
from minesweeper.minesweeper import start_minesweeper

def main():
    print("Before true")
    while True:
        clear()
        print("1. Play Wordle")
        print("2. Play Minesweeper")
        print("17. Exit program")
        choice = input("> ")
        if choice == "1":
            start_wordle()
        elif choice == "2":
            start_minesweeper()
        elif choice == "17":
            exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()