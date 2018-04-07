import pyttsx3 as pyttsx
import shelve
import random
import numpy as np

class WordCycle(object):
    DICT_EXT="dict"
    LINE_SPLITTER=":"
    WORD_SPLITTER=","

    def __init__(self, file_name, base_language, learning_language):
        """
        Opens the dictionary, 
        selects the set of the words usin filter
        Opens the statistics file
        Pair the statistics to the words
        creates two instance variables:
            word_dict   <dictionary>
                            "id": ["part_of_speach", "base_word", [[word, and, its, forms]]]
            recent_stat <dictionary>
                            "id": [[1,0,0,1],[0, 0, 1]]
        """

        part_of_speach_filter="v"
        extra_filter=""

        self.base_language=base_language
        self.learning_language=learning_language

        self.dict_file_name=file_name+"." + self.__class__.DICT_EXT
        self.stat_file_name=file_name

        #
        # read, parse and filter the necesarry words
        #
        # output: word_dict
        try:
            with open( self.dict_file_name ) as f:
                self.word_dict={}
                for line in f:
                    element_list=line.strip().split(self.__class__.LINE_SPLITTER)
                    if element_list[1].lower() == part_of_speach_filter.lower():
                        self.word_dict[element_list[0]]=(element_list[1], element_list[2], list(map(str.strip, element_list[3].strip().split(self.__class__.WORD_SPLITTER) ) ) )
                
        except FileNotFoundError as e:
            print( e )
            exit()

        #now in the word_dict found all filtered words by line

        with shelve.open(self.stat_file_name, writeback=True) as db:

            #
            # get the statistics for the filtered word list
            #
            # output: db
            self.recent_stat={}

            for word_id, _ in self.word_dict.items():
        
                # create the record if it does not exist
                try:
                    # remove all empty tuples
                    db[word_id] = [t for t in db[word_id] if not all(t)]

                except Exception as e:

                    #as there has not been record creates an empty
                    db[word_id] = []
    
                #append the actual empty list for statistics
                db[word_id].append([])
    
                #updates
                self.recent_stat[word_id]=db[word_id][-1]   

    def set_answer(self, word_id, success):
        """
        input:  word_id: string
                success: boolean
                    True    -good answer
                    False   -wrong anser
        """
        with shelve.open(self.stat_file_name, writeback=True) as db:

            #updates db
            db[word_id][-1].append(1 if success else 0)

            #updates recent_stat variable
            self.recent_stat[word_id]=db[word_id][-1]

    def get_next(self):
        """
        Gives back a randomly chosen word from the filtered wordlist

        output: tuple
                    word id
                    [part_of_speach, translation,  [word, and, its, forms]]
        """
        word_id=self.get_random_word(self.recent_stat)
        return word_id, self.word_dict[ word_id ]

    def get_recent_stat(self, word_id):
        """
        Gives back the recent statistics of a word by id

        input:  word_id: string
        output: tuple of recent statistics (1,0,0,1)                    
        """
        return self.recent_stat[word_id]

    def check_answer(self, word_id, answer):
        """
        input:  word_id: string
                answer: list
                    [word, and, its, forms]

        output: boolean
                    True:   if the answer is acceptable
                    False:  if the answer is not acceptable
                list
                    [first, wrong, position, of, words]
        """
        question=self.word_dict[word_id][2]
        zipped_list= list(zip( question, answer + [" "*len(i) for i in question][len(answer):] ))
        diff_list=[[i for i in range(len(j[1])) if j[1][i] != j[0][i]] for j in zipped_list]
        if sum([1 for i in diff_list if len(i)!=0]) == 0:
            return True, diff_list
        else:
            return False, diff_list

    def get_random_word(self, stat_list):
        """
        Returns the identifier of a random word in the list.
        The word with higher points get higher chance to be selected.
        The points depend on the good and bad answers

        input: 
                stat_list - [dictionary]    key:    word id
                                            value:  []
        output:
                a random word id from the list
        """
        #empty if every element have at least one 1 in the list
        first_round_list=[i for i in stat_list if not any(stat_list[i])]

        #if not empty
        if any(first_round_list):

            #all element with same chance - must be changed
            return random.choice(first_round_list)
    
        #if empty - chances must be taken by statistics
        else:
            return random.choice([ k for k, v in stat_list.items() for i in range(self.get_points(v))])

    def get_points(self, stat):
        """
        Calculates the points of the "stat" list
        "stat" contains 0s and 1s representing the bad and good answers
        for a specific word in the recent session.
        More points mean worse answers.
        The following generate points:
            -number of the tralling 0s
            -number of the wrong answers
            -number of the wrong answers after a good answer
    
        input:
                stat: [list] -  0: bad answer
                                1: good answer
        """
    
        points=1
        # counts not knowing last n times(ends with 0)
        points += len(stat)-len("".join(map(str, stat)).rstrip("0"))    
        #   #counts all not knowings (0s)
        #   points += len(stat)-sum(stat)
        # counts difference between 1 and 0
        points += max(sum([1 for i in stat if i == 0])*2 - len(stat), 0)
        # counts all forgetting (1 -> 0)
        points += np.sum(np.diff(stat) == -1)          

        return points


#if __name__ == "__main__":
    #myWordCycle=WordCycle()
    #print(myWordCycle.get_next())
