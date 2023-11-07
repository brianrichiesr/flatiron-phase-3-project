import curses
import time
import random
import re
from database.orm import Database

def start_typeracer(user):
    curses.wrapper(lambda x: typeracer(x,user))

def typeracer(stdscr,user):
    curses.resizeterm(30, 60)
    # paragraphs = ["Business casual is an ambiguously defined dress code that has been adopted by many professional and white-collar workplaces in Western countries. It entails neat yet casual attire and is generally more casual than informal attire but more formal than casual or smart casual attire. Casual Fridays preceded widespread acceptance of business casual attire in many offices", "A teacher's professional duties may extend beyond formal teaching. Outside of the classroom teachers may accompany students on field trips, supervise study halls, help with the organization of school functions, and serve as supervisors for extracurricular activities. In some education systems, teachers may have responsibility for student discipline.", "The basic technique stands in contrast to hunt and peck typing in which the typist keeps his or her eyes on the source copy at all times. Touch typing also involves the use of the home row method, where typists keep their wrists up, rather than resting them on a desk or keyboard (which can cause carpal tunnel syndrome). To avoid this, typists should sit up tall, leaning slightly forward from the waist, place their feet flat on the floor in front of them with one foot slightly in front of the other, and keep their elbows close to their sides with forearms slanted slightly upward to the keyboard; fingers should be curved slightly and rest on the home row.", "When we talk about motivating others, the justification is the end result (either we want to avoid the pain or go towards pleasure) or what we want to get the person to do. How we achieve the end result, are our alternatives. As a manager, we need to understand the other person's justification and then come up with alternatives. We may then choose the right alternative. However, in general, we choose the first or the emotionally satisfying one. Typically people stop at this level of analysis and start to act. But a good manager would think of the following also: Will the action guarantee the consequence? What about other unintended consequences? This requires a certain experience. Are we capable of doing this action? Intention and the selection of the most ideal alternative do not guarantee execution, if we do not have the skills and the experience. Most motivational tactics fail, because without execution capability, they is only wishful thinking."]
    paragraphs = ['hello']
    solution = random.choice(paragraphs)
    start_time = time.time()
    length_solution = len(solution)
    mistakes = 0
    is_playing = True
    def guess(guess,solution):
        if guess.lower() == solution[0].lower():
            return True
        return False
    
    regex = re.compile(r"[^a-zA-Z]")

    def alpha(string):
        if regex.search(string):
            return False
        return True
    
    while is_playing:
        if(not len(solution) == 0):
            stdscr.clear()
            stdscr.addstr(0,0,solution)
            stdscr.refresh()
            inp = chr(stdscr.getch())
            if(guess(inp,solution)):
                solution = solution[+1:]
            else:
                # import ipdb;ipdb.set_trace()
                if(alpha(inp)):
                    mistakes +=1
        else:
            end_time = time.time()
            wpm = length_solution/(round(end_time-start_time,0)/60)
            stdscr.clear()
            stdscr.addstr(0,0,f"Game over! You made {mistakes} mistake{'s' if mistakes != 1 else ''}.")
            stdscr.addstr(1,0,f"You were {((length_solution - mistakes)/length_solution) * 100:.2f}% accurate!")
            stdscr.addstr(2,0,f"You typed at {wpm} wpm")
            score = round(((((length_solution - mistakes)/length_solution) * 100)/(end_time-start_time) * 2.2),2)
            Database.insert_game(("Typeracer",round(end_time-start_time,2),3,score,Database.get_player(user.username)[0]))
            stdscr.refresh()
            time.sleep(3.5)
            is_playing = False
        
    