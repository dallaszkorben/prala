import time
import curses
for i in range(10):
    time.sleep(0.2) 
    #curses.initscr()
    #curses.curs_set(1)
    #curses.setsyx(-1, -1)
    #curses.resetty()

    print("\033[%d;%dH" % (5, 5))
    print ("\r Loading... {0}".format(i), end="")