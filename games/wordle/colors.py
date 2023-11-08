# Import module to give color to text
import curses

# Function that takes the user's guess and the solution as arguments
def color_word(user_guess, solution):
    # Makes the guess and solution the same case
    user_guess.upper()
    solution.upper()
    # List to keep track of the color of each letter of user's guess
    colors = []
    # List of False values
    used = [False] * len(solution)

    # Iterate through each letter of user's guess to check for exact match of letter at
    #   each position
    for idx, letter in enumerate(user_guess):
        if letter == solution[idx]:
            colors.append(1)  # Green for correct position
            used[idx] = True
        else:
            colors.append(0)  # Default to no color
    
    # Iterate through each letter of user's guess to check if the letter that were not
    #   exact matches, were somewhere else in the solution
    for idx, letter in enumerate(user_guess):
        if colors[idx] == 0:
            for i, target_letter in enumerate(solution):
                if letter == target_letter and not used[i]:
                    colors[idx] = 2  # Yellow for correct letter in the wrong position
                    used[i] = True
                    break
    
    return colors

# Function that takes 3 arguments
def print_colored_word(stdscr, user_guess, compare):

    # Iterate through each letter of the user's guess and add correct color to each letter
    for letter, color in zip(user_guess, color_word(user_guess, compare)):
        if color == 1:
            stdscr.addch(letter, curses.color_pair(color))
        elif color == 2:
            stdscr.addch(letter, curses.color_pair(color))
        else:
            stdscr.addch(letter)