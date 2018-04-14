import pyttsx3 as pyttsx
import shelve
import random
import numpy as np

class FiteredDictionary(object):
    DICT_EXT="dict"
    RECORD_SPLITTER=":"
    WORD_SPLITTER=","

    def __init__(self, file_name, base_language, learning_language, part_of_speach_filter=""):
        """
        Opens the dictionary, 
        selects the set of the words usin filter
        Opens the statistics file
        Pair the statistics to the words
        creates two instance variables:
            word_dict   <dictionary>
                            "id": ["part_of_speach", "base_word", [[word, and, its, forms]]]
            recent_stat_list <dictionary>
                            "id": [[1,0,0,1],[0, 0, 1]]
        """

        #part_of_speach_filter="v"
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
                    element_list=line.strip().split(self.__class__.RECORD_SPLITTER)
                    if len(part_of_speach_filter) == 0 or element_list[1].lower() == part_of_speach_filter.lower():
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
            self.recent_stat_list={}

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
                self.recent_stat_list[word_id]=db[word_id][-1]   

    def get_next_random_record(self):
        """
        Gives back a randomly chosen line object from the filtered wordlist

        output: WordLine object
        """
        word_id=self.get_random_id(self.recent_stat_list)

        return Record( self.base_language, self.learning_language, word_id, self.word_dict[ word_id ], self.recent_stat_list[ word_id ])
        #return word_id, self.word_dict[ word_id ]

    def add_result_to_stat(self, word_id, success):
        """
        input:  word_id: string
                success: boolean
                    True    -good user_answer
                    False   -wrong anser
        """
        with shelve.open(self.stat_file_name, writeback=True) as db:

            """
            #updates db
            db[word_id][-1].append(1 if success else 0)
            #updates recent_stat_list variable
            self.recent_stat_list[word_id]=db[word_id][-1]
            """

            #updates db
            self.recent_stat_list[word_id].append(1 if success else 0)

            #updates recent_stat_list variable
            db[word_id][-1]=self.recent_stat_list[word_id]

    def get_random_id(self, stat_list):
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

    def get_points(self, recent_stat):
        """
        Calculates the points of the "recent_stat" list
        "recent_stat" contains 0s and 1s representing the bad and good answers
        for a specific word in the recent session.
        More points mean worse answers.
        The following generate points:
            -number of the tralling 0s
            -number of the wrong answers
            -number of the wrong answers after a good user_answer
    
        input:
                [list]: recent_stat: 
                            -   0: bad user_answer
                            -   1: good user_answer
        """
        points=1
        # counts not knowing last n times(ends with 0)
        points += len(recent_stat)-len("".join(map(str, recent_stat)).rstrip("0"))    
        #   #counts all not knowings (0s)
        #   points += len(recent_stat)-sum(recent_stat)
        # counts difference between 1 and 0
        points += max(sum([1 for i in recent_stat if i == 0])*2 - len(recent_stat), 0)
        # counts all forgetting (1 -> 0)
        points += np.sum(np.diff(recent_stat) == -1)          

        return points

    def get_recent_stat_list(self):
        """
        Gives back the statistics of the last cycle

        output: [list]
                        list[0]:    numbers of the questions
                        list[1]:    numbers of the good answers
        """
        pass

class Record(object):

    def __init__(self, base_language, learning_language, word_id, word, recent_stat):
        """
            base_language       - string
            learning_language   - string
            word_id             - integer
            word                - list:     [part_of_speach, base_word,  [word, and, its, forms]]
        """
        self.base_language = base_language
        self.learning_language = learning_language
        self.word_id = word_id
        
        self.part_of_speach = word[0]
        self.base_word = word[1]
        self.learning_words = word[2]

        #self.word = word
        self.recent_stat = recent_stat

    def get_recent_stat(self):
        """
        Gives back the recent statistics of the actual Record

        output: tuple of recent statistics (1,0,0,1)                    
        """
        return self.recent_stat

    def check_answer(self, user_answer):
        """
        input:  user_answer: list
                    ['word', 'and', 'its', 'forms']

        output: boolean
                    True:   if the user_answer is acceptable
                    False:  if the user_answer is not acceptable
                list
                    [first, wrong, position, of, words]
        """
        zipped_list= list(zip( self.learning_words + [" "*len(i) for i in user_answer][len(self.learning_words):], user_answer + [" "*len(i) for i in self.learning_words][len(user_answer):] ) )
        zipped_list=[ (i[0] + (" "*len(i[1]))[len(i[0]):], i[1] + (" "*len(i[0]))[len(i[1]):] ) for i in zipped_list]

        diff_list=[[i for i in range(len(j[1])) if j[1][i] != j[0][i]] for j in zipped_list]
        if sum([1 for i in diff_list if len(i)!=0]) == 0:
            return True, diff_list
        else:
            return False, diff_list

    def say_out_base(self):
        """
        It says out the text in the list on the 'base language'
        """
        engine = pyttsx.init()

        engine.setProperty('voice', self.base_language)		#voice id
        #engine.setProperty('rate', 150)
        #engine.setProperty('volume', 1)
        
        #TODO parameter to ENUM
        engine.say(self.base_word)
        engine.runAndWait()

    def say_out_learning(self):
        """
        It says out the text in the list on the 'learning language'
        """
        engine = pyttsx.init()

        engine.setProperty('voice', self.learning_language)		#voice id
        
        #TODO parameter to ENUM
        [engine.say(i) for i in self.learning_words]
        engine.runAndWait()


#if __name__ == "__main__":
    #myFiteredDictionary=FiteredDictionary()
    #print(myFiteredDictionary.get_next())