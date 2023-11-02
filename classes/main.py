import curses

def main(stdscr):
    # Set up the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    stdscr.timeout(100)  # Set a timeout for getch (100 milliseconds)
    all = ""

    while True:
        key = stdscr.getch()
        
        if key != -1:
            if key == 127:
                all = all[:-1]

            



            elif len(all) < 5 and chr(key).isalpha():  
                all += chr(key)
            
            if key == 10:
                if len(all) == 5:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f'You chose: {all}')
                    stdscr.refresh()
                    game.checkwin()
                    all = ""
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f'Current word: {all}')
                stdscr.refresh()


        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
