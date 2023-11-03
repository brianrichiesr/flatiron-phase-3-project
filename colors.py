import curses

def color_word(word, target_word):
    word.upper()
    target_word.upper()
    colors = []
    used = [False] * len(target_word)

    for idx, letter in enumerate(word):
        if letter == target_word[idx]:
            colors.append(1)  # Green for correct position
            used[idx] = True
        else:
            colors.append(0)  # Default to no color

    for idx, letter in enumerate(word):
        if colors[idx] == 0:
            for i, target_letter in enumerate(target_word):
                if letter == target_letter and not used[i]:
                    colors[idx] = 2  # Yellow for correct letter in the wrong position
                    used[i] = True
                    break
    
    return colors

def print_colored_word(stdscr,word,compare):
    for letter, color in zip(word, color_word(word,compare)):
        if color == 1:
            stdscr.addch(letter, curses.color_pair(color))
        elif color == 2:
            stdscr.addch(letter, curses.color_pair(color))
        else:
            stdscr.addch(letter)