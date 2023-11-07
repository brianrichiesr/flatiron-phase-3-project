import curses
import time

def start_typeracer():
    curses.wrapper(lambda x: typeracer(x))

def typeracer(stdscr):
    solution = "The quick brown fox jumped over the lazy dog."
    start_time = time.time()
    length_solution = len(solution)
    mistakes = 0
    is_playing = True
    def guess(guess,solution):
        if guess.lower() == solution[0].lower():
            # game['index'] += 1
            return True
        return False
    
    while is_playing:
        if(not len(solution) == 0):
            stdscr.clear()
            stdscr.addstr(0,0,solution)
            stdscr.refresh()
            inp = chr(stdscr.getch())
            if(guess(inp,solution)):
                solution = solution[+1:]
            else:
                mistakes +=1
        else:
            end_time = time.time()
            wpm = length_solution/(round(end_time-start_time,0)/60)
            stdscr.clear()
            stdscr.addstr(0,0,f"Game over! You made {mistakes} mistake{'s' if mistakes > 1 else ''}.")
            stdscr.addstr(1,0,f"You were {((length_solution - mistakes)/length_solution) * 100:.2f}% accurate!")
            stdscr.addstr(2,0,f"You typed at {wpm} wpm")
            stdscr.refresh()
            time.sleep(2)
            is_playing = False
            
    