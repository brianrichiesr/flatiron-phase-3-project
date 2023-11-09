import curses
import time
import random
import re
from database.orm import Database

#Start game with wrapper so it can be started from cli
def start_typeracer(user):
    curses.wrapper(lambda x: typeracer(x,user))

#Main game function
def typeracer(stdscr,user):
    stdscr.nodelay(0)
    stdscr.clear()
    #Resize terminal so text wraps easier
    curses.resizeterm(30, 60)
    #All texts
    paragraphs = ["In another experiment involving students, respondents were asked about likely future outcomes for themselves and their roommates. They typically had very rosy views about their own futures, which they imagined to include successful careers, happy marriages, and good health. When asked to speculate about their roommates' futures, however, their responses were far more realistic. The roommates were believed to be far more likely to become alcoholics, suffer illnesses, get divorced, and experience a variety of other unfavorable outcomes.","Most people can motivate themselves to do things simply by knowing that those things need to be done. But not me. For me, motivation is this horrible, scary game where I try to make myself do something while I actively avoid doing it. If I win, I have to do something I don't want to do. If I lose, I'm one step closer to ruining my entire life. And I never know whether I'm going to win or lose until the last second.","I woke up this morning with the sundown shining in. I found my mind in a brown paper bag within. I tripped on a cloud and fell eight miles high. I tore my mind on a jagged sky. I just dropped in to see what condition my condition was in.","If they say, who cares if one more light goes out in a sky of a million stars? It flickers, flickers. Who cares when someone's time runs out if a moment is all we are. We're quicker, quicker. Who cares if one more light goes out? Well, I do.","Business casual is an ambiguously defined dress code that has been adopted by many professional and white-collar workplaces in Western countries. It entails neat yet casual attire and is generally more casual than informal attire but more formal than casual or smart casual attire. Casual Fridays preceded widespread acceptance of business casual attire in many offices", "A teacher's professional duties may extend beyond formal teaching. Outside of the classroom teachers may accompany students on field trips, supervise study halls, help with the organization of school functions, and serve as supervisors for extracurricular activities. In some education systems, teachers may have responsibility for student discipline.", "The basic technique stands in contrast to hunt and peck typing in which the typist keeps his or her eyes on the source copy at all times. Touch typing also involves the use of the home row method, where typists keep their wrists up, rather than resting them on a desk or keyboard (which can cause carpal tunnel syndrome). To avoid this, typists should sit up tall, leaning slightly forward from the waist, place their feet flat on the floor in front of them with one foot slightly in front of the other, and keep their elbows close to their sides with forearms slanted slightly upward to the keyboard; fingers should be curved slightly and rest on the home row.", "When we talk about motivating others, the justification is the end result (either we want to avoid the pain or go towards pleasure) or what we want to get the person to do. How we achieve the end result, are our alternatives. As a manager, we need to understand the other person's justification and then come up with alternatives. We may then choose the right alternative. However, in general, we choose the first or the emotionally satisfying one. Typically people stop at this level of analysis and start to act. But a good manager would think of the following also: Will the action guarantee the consequence? What about other unintended consequences? This requires a certain experience. Are we capable of doing this action? Intention and the selection of the most ideal alternative do not guarantee execution, if we do not have the skills and the experience. Most motivational tactics fail, because without execution capability, they is only wishful thinking."]
    #Get random text
    solution = random.choice(paragraphs)
    #Init timer
    start_time = time.time()
    #Get length of solution for later
    length_solution = len(solution.split())
    #Init mistakes to 0
    mistakes = 0
    #Main game loop var
    is_playing = True
    #Guess function to check if letter typed matches first letter
    def guess(guess,solution):
        if guess == solution[0]:
            return True
        return False
    
    #Regex so you can only type a-z
    regex = re.compile(r"[^a-zA-Z]")

    #Function that uses regex to make sure no non alpha
    def alpha(string):
        if regex.search(string):
            return False
        return True
    
    #Main game loop
    while is_playing:
        #If text has any letters left
        if (len(solution)):
            #Clear screen
            stdscr.clear()
            #Add text to page
            stdscr.addstr(0,0,solution)
            stdscr.refresh()
            #Get input
            inp = stdscr.getch()
            # if inp != curses.ERR:
                
            if(guess(chr(inp),solution)):
                #if input is equal to first letter, remove the letter
                solution = solution[+1:]

            #Else, if input is alphabetical, mistakes + 1
            elif alpha(chr(inp)):
                mistakes +=1

        else:
            #Get current time for end time
            end_time = time.time()
            #Calculate words per minute
            wpm = length_solution/(round(end_time-start_time,0)/60)
            #Clear screen
            stdscr.clear()
            #Display stats
            stdscr.addstr(0,0,f"Game over! You made {mistakes} mistake{'s' if mistakes != 1 else ''}.")
            stdscr.addstr(1,0,f"You were {((length_solution - mistakes)/length_solution) * 100:.2f}% accurate!")
            stdscr.addstr(2,0,f"You typed at {wpm:.2f} wpm")
            score = round(((((length_solution - mistakes)/length_solution) * 100)/(end_time-start_time) * 2.2),2)
            #Add game to db
            Database.insert_game(("Typeracer",round(end_time-start_time,2),3,score,Database.get_player(user.username)[0]))
            stdscr.refresh()
            time.sleep(3.5)
            #Break from main loop back to cli
            is_playing = False