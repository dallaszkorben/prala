import itertools
from prala import WordCycle

#myWordCycle=WordCycle()
#stat_list=[list(i) for i in list(itertools.product([0,1], repeat=3))]
#print([(myWordCycle.get_points(i), i) for i in stat_list])
#print( *sorted([(myWordCycle.get_points(i), i) for i in stat_list], key=lambda x: x[0], reverse=True), sep="\n" )

#stat=[0,0,1]
#print( max(sum([1 for i in stat if i == 0])*2 - len(stat), 0) )



#answer=["abc", "def"]
#question=[1,[1,2,["abc", "deg", "mnopqr","stuvwxyz","a"]]]

answer=['ABCDE', 'FGHI', 'JKL', 'MN', 'O']
question=("1",['v', 'aaa', ['ABCDE', 'FGHI', 'JKL', 'MN', 'O']])
 

zipped_list= list(zip( question[1][2], answer + [" "*len(i) for i in question[1][2]][len(answer):] ))
print(zipped_list)

#diff_list=[]
#for j in zipped_list:
#    diff_list.append( [i for i in range(len(j[1])) if j[1][i] != j[0][i]] )

diff_list=[[i for i in range(len(j[1])) if j[1][i] != j[0][i]] for j in zipped_list]

print(diff_list)


