import sys
from unicurses import *

def menu(scr):
    scr.nodelay(0)
    scr.clear()
    selection = -1
    option = 0
    while selection<0:
        graphics= [0]*5
        graphics[option] = A_REVERSE
        scr.addstr(0,dims[1]/2-3,"Login")
        scr.refresh()
        option = screen.getch()

def main():
    scr = initscr()
    start_color()
    init_pair(1, COLOR_RED, COLOR_BLACK)
    keypad(scr, True)
    noecho()
    curs_set(False)
    nodelay(scr,0)
    clear()
    selection = -1
    option = 0
    while selection<0:
        graphics = [0]*4
        graphics[option] = A_REVERSE
        move(0,0)
        addstr("Login",graphics[0] + color_pair(1))
        move(1,0)
        addstr("Queue",graphics[1] + color_pair(1))
        move(2,0)
        addstr("Buffer",graphics[2] + color_pair(1))
        move(3,0)
        addstr("Logout",graphics[3] + color_pair(1))
        
        refresh()
        action = getch()
        if action == KEY_UP:
            option = (option-1) % 4
        elif action == KEY_DOWN:
            option = (option+1) % 4
        elif action == ord('\n'):
            selection = option

        move(5,0)
        addstr(str(option))
        if selection == 0:
            break;
        
    endwin()
    
if __name__ == "__main__":
    main()
