import itertools
from prala import WordCycle

myWordCycle=WordCycle()
stat_list=list(itertools.product([0,1], repeat=3))
print([[1, list(i)] for i in stat_list])