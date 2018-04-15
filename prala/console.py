import sys
import os
import re
from iso639 import to_name

from prala.core import FilteredDictionary
from prala.core import Record
from prala.accessories import Property

class ConsolePrala(object):
    COLOR_DEFAULT="\033[00m"
    COLOR_QUESTION="\033[1;37m"
    COLOR_INPUT="\033[1;34m"
    COLOR_RESULT_STATUS_WRONG="\033[0;31m"
    COLOR_RESULT_STATUS_RIGHT="\033[0;32m"
    COLOR_GOOD_ANSWER_WRONG="\033[0;31m"
    COLOR_GOOD_ANSWER_RIGHT="\033[0;32m"
    COLOR_STAT="\033[1;33m"
    COLOR_CORRECTION_RIGHT="\033[0;37m"
    COLOR_CORRECTION_WRONG="\033[1;31m"
    COLOR_STAT="\033[1;33m"

    POSITION_QUESTION="\033[10;10H"
    POSITION_INPUT="\033[11;10H"
    POSITION_RESULT_STATUS="\033[12;10H"
    POSITION_CORRECTION="\033[18;10H"
    POSITION_GOOD_ANSWER="\033[16;10H"
    POSITION_STAT="\033[21;10H"

    STATUS_WRONG="WRONG"
    STATUS_RIGHT="RIGHT"

    def __init__( self, file_name, base_language, learning_language, part_of_speach_filter="" ):

        self.myFilteredDictionary=FilteredDictionary(file_name, base_language, learning_language, part_of_speach_filter) 

    def round(self):

        self.clear_console()
        record=self.myFilteredDictionary.get_next_random_record()

        # shows the question word
        self.out_question(record.base_word + " - (" + str(len(record.learning_words) ) + ")")
        record.say_out_base()

        # replace every alphabetic character to _ to show under cursor
        template=re.sub("[^, \!]", "_", ", ".join(record.learning_words))
        line=[ i.strip() for i in self.get_input(template).split(",")]
        result=record.check_answer(line)
        # write back the stat
        self.myFilteredDictionary.add_result_to_stat(record.word_id,result[0])
        if result[0]:
            self.out_good_answer_right(record.learning_words)
        else:
            self.out_correction(result[1], line, record.learning_words)
            self.out_good_answer_wrong(record.learning_words)

        #shows statistics
        overall=self.myFilteredDictionary.get_recent_stat_list()
        overall_str=str(overall[1]) + "/" + str(overall[0]) + ("/" + str(overall[2]) if overall[2] > 0 else "") + " (" + str(int(100 * overall[1] / overall[0])) + "%)"
        actual=record.get_recent_stat()        
        self.out_stat(overall_str, actual)
        record.say_out_learning()
        #waitin for a click to continue
        input()

    def clear_console(self):
        sys.stdout.write("\033[2J")

    def out_question(self, question):
        sys.stdout.write(type(self).POSITION_QUESTION)
        sys.stdout.write(type(self).COLOR_QUESTION)
        print(question)
        sys.stdout.write(type(self).COLOR_DEFAULT)

    def get_input(self, template):
        sys.stdout.write(type(self).POSITION_INPUT)
        sys.stdout.write(type(self).COLOR_INPUT)
        print(template)
        sys.stdout.write(type(self).POSITION_INPUT)
        
        return input()

    def out_result_status(self, status):
        sys.stdout.write(type(self).POSITION_RESULT_STATUS)
        if status:
            sys.stdout.write(type(self).COLOR_RESULT_STATUS_RIGHT)
            print(type(self).STATUS_RIGHT)
        else:
            sys.stdout.write(type(self).COLOR_RESULT_STATUS_WRONG)
            print(type(self).STATUS_WRONG)

        sys.stdout.write(type(self).COLOR_DEFAULT)

    def out_good_answer_right(self, answer):
        sys.stdout.write(type(self).POSITION_GOOD_ANSWER)
        sys.stdout.write(type(self).COLOR_GOOD_ANSWER_RIGHT)
        print( *answer, sep=", ")
        sys.stdout.write(type(self).COLOR_DEFAULT)
        self.out_result_status(True)

    def out_good_answer_wrong(self, answer):
        sys.stdout.write(type(self).POSITION_GOOD_ANSWER)
        sys.stdout.write(type(self).COLOR_GOOD_ANSWER_WRONG)
        print(*answer, sep=", ")

        sys.stdout.write(type(self).COLOR_DEFAULT)
        self.out_result_status(False)
   
    def out_stat(self, overall, specific):
        sys.stdout.write(type(self).POSITION_STAT)
        sys.stdout.write(type(self).COLOR_STAT)

        print( overall, specific)

        sys.stdout.write(type(self).COLOR_DEFAULT)
        
        
    def out_correction(self, result, line, learning_words):
        sys.stdout.write(type(self).POSITION_CORRECTION)

        zipped_list=list(zip( line + ["_"*len(i) for i in learning_words][len(line):], learning_words + [" "*len(i) for i in line][len(learning_words):] ) )
        for word_failed_position_pair in zip( [i[0] + ("_"*len(i[1]))[len(i[0]):] for i in zipped_list], result ):
            for pos in range(len(word_failed_position_pair[0])):
                if pos in word_failed_position_pair[1]:
                    sys.stdout.write(type(self).COLOR_CORRECTION_WRONG)
                else:
                    sys.stdout.write(type(self).COLOR_CORRECTION_RIGHT)
                print(word_failed_position_pair[0][pos], end="")
            print(", ", end="")
        sys.stdout.write(type(self).COLOR_DEFAULT)


    # this need to us the class with "with"
    def __enter__(self):
       return self

    # this need to us the class with "with"
    # the reason of using it "with" is to get back the default coursor color at the end
    def __exit__(self, exc_type, value, traceback):
      sys.stdout.write(type(self).COLOR_DEFAULT)
      print("")
      return isinstance(value, KeyboardInterrupt)	#Supress the KeyboardInterrupt exception

def main():

    if len(sys.argv) == 1:
        print()
        print("Usage:")
        print("python " + sys.argv[0] + " dict_file_name [part_of_speech_filter]")
        print("part of speech:")
        print("   n     -noun")
        print("   v     -verb")
        print("   j     -adjective")
        print("   b     -adverb")
        print("   r     -pronoun")
        print("   e     -preposition")
        print("   c     -conjunction")
        print("   i     -interjection")
        print("   a     -article")
        
        exit()

    file_name = sys.argv[1]

    if len(sys.argv) >= 3:
        part_of_speech = sys.argv[2]
    else:
        part_of_speech = ""

    DEFALULT_BASE_LANGUAGE="en"
    DEFALULT_LEARNING_LANGUAGE="sv"

    file=os.path.join(os.getcwd(),'config.ini')
    property=Property(file)
    base_language=to_name(property.get('languages', 'base_language', DEFALULT_BASE_LANGUAGE)).lower()
    learning_language=to_name(property.get('languages', 'learning_language', DEFALULT_LEARNING_LANGUAGE)).lower()    

   # the reason of using it "with" is to get back the default coursor color at the end
    with ConsolePrala(file_name, base_language, learning_language, part_of_speech) as cp:
      while True:
         cp.round()

#if __name__ == "__main__":
#    main()
