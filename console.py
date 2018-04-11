import sys
from prala import FiteredDictionary
from prala import Record

COLOR_DEFAULT="\033[00m"
COLOR_QUESTION="\033[1;37m"
COLOR_INPUT="\033[1;34m"
COLOR_GOOD_ANSWER_RIGHT="\033[0;32m"
COLOR_GOOD_ANSWER_WRONG="\033[0;31m"
COLOR_STAT="\033[1;33m"

POSITION_QUESTION="\033[10;10H"
POSITION_INPUT="\033[11;10H"
POSITION_GOOD_ANSWER="\033[12;10H"

def clear_console():
    sys.stdout.write("\033[2J")

def out_question(question):
    sys.stdout.write(POSITION_QUESTION)
    sys.stdout.write(COLOR_QUESTION)
    print(question)
    sys.stdout.write(COLOR_DEFAULT)

def get_input():
    sys.stdout.write(POSITION_INPUT)
    sys.stdout.write(COLOR_INPUT)
    return input()

def out_good_answer_right(answer):
    sys.stdout.write(POSITION_GOOD_ANSWER)
    sys.stdout.write(COLOR_GOOD_ANSWER_RIGHT)
    print(answer)
    sys.stdout.write(COLOR_DEFAULT)

def out_good_answer_wrong(answer):
    sys.stdout.write(POSITION_GOOD_ANSWER)
    sys.stdout.write(COLOR_GOOD_ANSWER_WRONG)
    print(answer)
    sys.stdout.write(COLOR_DEFAULT)

myFilteredDictionary=FiteredDictionary("base", 'hungarian', 'swedish') 

while True:
    clear_console()
    record=myFilteredDictionary.get_next_random_record()
    out_question(record.base_word + " - (" + str(len(record.learning_words) ) + ")")
    record.say_out_base()    
    line=[ i.strip() for i in get_input().split(",")]
    result=record.check_answer(line)
    if result[0]:
        out_good_answer_right(record.learning_words)
    else:
        out_good_answer_wrong(record.learning_words)
    record.say_out_learning()
    input()