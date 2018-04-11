import time
import curses
"""
for i in range(10):
    time.sleep(0.2) 
    #curses.initscr()
    #curses.curs_set(1)
    #curses.setsyx(-1, -1)
    #curses.resetty()

    print("\033[%d;%dH" % (5, 5))
    print ("\r Loading... {0}".format(i), end="")ff
"""

class Called:
    def __init__(self, a):
        self.a=a
        #self.a.append("world")


class Caller:

    def __init__(self):
        self.array=[[],[]]
        self.array[0].append("hello")
    
        c=Called(self.array[0])

        #self.array[0].append("world")
        self.array[0]=["hello", "world"]

        #print(self.array)
        print(c.a)

#c=Caller()

from prala import FiteredDictionary

myFilteredDictionary=FiteredDictionary("testfile", 'hungarian', 'swedish','v') 
next=myFilteredDictionary.get_next_random_record()
myFilteredDictionary.set_answer_result(next.word_id, True)
myFilteredDictionary.set_answer_result(next.word_id, False)
myFilteredDictionary.set_answer_result(next.word_id, True)
#print(next.recent_stat)
#print(myFilteredDictionary.recent_stat_list)
