import curses
from collections import Counter

def print_colored_word(stdscr, word, compare):
    colors = []
    letters = dict(Counter(word))
    print(letters)
    for idx,letter in enumerate(compare):
        if word[idx] == compare[idx]:
            colors.append(1)
        elif compare[idx] in word:
            #! TODO
            #Check count of letters to determine how many yellow letters are needed
            #implement print colored word into main game after enter press
            #limit main game to 6 guesses
            #do something on win
            colors.append(2)
        else:
            colors.append(3)

    for letter, color_pair in zip(word, colors):
        stdscr.addch(letter, curses.color_pair(color_pair))
        stdscr.refresh()

def main(stdscr):
    # Initialize curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Define the word and colors for each letter

    # Call the function to print the word with colors
    print_colored_word(stdscr, "elloh", "Hollo")

    stdscr.getch()  # Wait for user input

if __name__ == "__main__":
    curses.wrapper(main)
