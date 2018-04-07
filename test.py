import itertools
from prala import WordCycle

myWordCycle=WordCycle()

question=("1",['v', 'aaa', ['ABCDE', 'FGHI', 'JKL', 'MN', 'O']])
#myWordCycle.set_answer(question, False)
#myWordCycle.set_answer(question, True)
#myWordCycle.set_answer(question, False)
print(myWordCycle.get_stat("13"))