import pyttsx3 as pyttsx
import shelve
import random
from functools import reduce 
import numpy as np

part_of_speach=["verb", "noun", "adjektive", "adverb", "pronoun", "preposition", "conjunction", "determiner", "exclamation"]

STAT_DB_EXT="dat"
DICT_EXT="dic"
LINE_SPLITTER=":"
WORD_SPLITTER=","

base_language="hu"
learn_leanguage="sv"
dict_name="base"
part_of_speach_filter="v"

file_name=dict_name+"_"+base_language+"_"+learn_leanguage+"." + DICT_EXT

#
# read and filter the necesarry words
#
# output: word_dict
try:
    with open( file_name ) as f:
        word_dict={}
        for line in f:
            element_list=line.strip().split(LINE_SPLITTER)
            if element_list[1].lower() == part_of_speach_filter.lower():
                word_dict[element_list[0]]=(element_list[1], element_list[2], element_list[3].strip().split(WORD_SPLITTER) ) 
                    
                
except FileNotFoundError as e:
    print( e )
    exit()

#now in the word_dict found all filtered words by line


with shelve.open(dict_name+"_"+base_language+"_"+learn_leanguage+"."+STAT_DB_EXT, writeback=True) as db:

    #
    # get the statistics for the filtered word list
    #
    # output: db
    recent_stat={}
    for word_id, word_values in word_dict.items():
        
        # create the record if it does not exist
        try:
            # remove all empty tuples
#            print(db[word_id])
            db[word_id] = [t for t in db[word_id] if all(t)]
#            print(db[word_id])
#            print()
        except Exception as e:
#            print("hiba: {0}".format(e.args) 
            #as there has not been record creates an empty
            db[word_id] = []
    
        #append the actual empty list for statistics
        db[word_id].append([])
        # now the db is filled up - add a new list for test
        #db[word_id]=[[0,0,0,1], [0,1,1,0,0,1]]

        '''
        good=0  # good answers
        bad=0   # bad answers
        back=0  # bad answers after good
        for t in db[word_id]:
            good+=sum(t)
            bad+=len(t)-sum(t)

            i=0
            for j in t:
                if j == 0 and i == 1:
                    back = +1
                    i = 0
                elif j == 1:
                    i = 1
        recent_stat[word_id]=[good, bad, back, []]
        '''

        recent_stat[word_id]=db[word_id][-1]

#print(recent_stat["1"])
recent_stat["1"]=[0,0,0]
recent_stat["2"]=[0,0,0]

#    priority="has not been selected", ""

#overall_how_bad=100*recent_stat[1]/(recent_stat[1]+recent_stat[2])
#overall_how_back=100*recent_stat[2]/(recent_stat[1]+recent_stat[2])


def get_random_word(stat_list):
    """
    input: 
           stat_list - [dictionary] key:    word id
                                    value:  []

    """
    #empty if every element have at least one 1 in the list
    first_round_list=[i for i in stat_list if not any(stat_list[i])]

    #if not empty
    if any(first_round_list):

        #all element with same chance - must be changed
        return random.choice(first_round_list)
    
    #if empty - chances must be taken by statistics
    else:
        return random.choice([ k for k, v in stat_list.items() for i in range(get_points(v))])


def get_points(stat):
    """
    input:
            stat: [list] -  0: bad answer
                            1: good answer
    """
    
    points=1

    #counts not knowing last n times(ends with 0)
    points += len(stat)-len("".join(map(str, stat)).rstrip("0"))    
    #counts all not knowings (0s)
    points += len(stat)-sum(stat)                   
    #counts all forgetting (1 -> 0)
    points += np.sum(np.diff(stat) == -1)          

    return points



#recent_stat["1"]=[0,1,0]
#recent_stat["2"]=[0,0,1]
#result=[ get_random_word(recent_stat) for i in range(1)]
#print(result)


##Testing get_random_word() method - 
#for i in range(100):
#    print( get_random_word(recent_stat) )

##Testing get_random_word() method - 2
list=[
    [1, [0,0,0]],
    [1, [0,0,1]],
    [1, [0,1,0]],
    [1, [0,1,1]],
    [1, [1,0,0]],
    [1, [1,0,1]],
    [1, [1,1,0]],
    [1, [1,1,1]]
]
for i in list:
    i.__setitem__(0,get_points(i[1]) )
list.sort(key=lambda x: x[0], reverse=True)
print(*list, sep="\n")


