import curses

def main(stdscr):
    curses.mousemask(curses.BUTTON1_CLICKED | curses.BUTTON3_CLICKED)
    stdscr.clear()
    stdscr.addstr(0, 0, "Left-click or Right-click to exit.")
    stdscr.refresh()
    
    while True:
        event = stdscr.getch()
        if event == curses.KEY_MOUSE:
            _, x, y, _, bstate = curses.getmouse()
            if bstate & curses.BUTTON1_CLICKED:
                stdscr.addstr(y, x, "Left-click detected!")
            elif bstate & curses.BUTTON3_CLICKED:
                stdscr.addstr(y, x, "Right-click detected!")
            stdscr.refresh()
        elif event == ord('q'):
            break

curses.wrapper(main)
