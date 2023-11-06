#!/usr/bin/env python
from clear_screen import clear
from wordle.wordle import start_wordle

# Print the menu of options when the user starts up the app
def main():
    print("Before true")
    while True:
        clear()
        print("1. Play Wordle")
        print("17. Exit program")
        choice = input("> ")
        if choice == "1":
            start_wordle()
        elif choice == "17":
            exit()
        else:
            print("Invalid choice")

# If this file is ran as the main and not imported it will run main()
if __name__ == "__main__":
    main()