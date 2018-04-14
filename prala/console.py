import sys
from prala import FiteredDictionary
from prala import Record

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

    POSITION_QUESTION="\033[10;10H"
    POSITION_INPUT="\033[11;10H"
    POSITION_RESULT_STATUS="\033[12;10H"
    POSITION_CORRECTION="\033[18;10H"
    POSITION_GOOD_ANSWER="\033[16;10H"

    STATUS_WRONG="WRONG"
    STATUS_RIGHT="RIGHT"

    def __init__( self, file_name, base_language, learning_language, part_of_speach_filter="" ):

        self.myFilteredDictionary=FiteredDictionary("base", 'hungarian', 'swedish') 

    def round(self):

        self.clear_console()
        record=self.myFilteredDictionary.get_next_random_record()

        # shows the question word
        self.out_question(record.base_word + " - (" + str(len(record.learning_words) ) + ")")
        record.say_out_base()
        line=[ i.strip() for i in self.get_input().split(",")]
        result=record.check_answer(line)
        if result[0]:
            self.out_good_answer_right(record.learning_words)
        else:
            self.out_correction(result[1], line, record.learning_words)
            self.out_good_answer_wrong(record.learning_words)
        record.say_out_learning()
        input()

    def clear_console(self):
        sys.stdout.write("\033[2J")

    def out_question(self, question):
        sys.stdout.write(type(self).POSITION_QUESTION)
        sys.stdout.write(type(self).COLOR_QUESTION)
        print(question)
        sys.stdout.write(type(self).COLOR_DEFAULT)

    def get_input(self):
        sys.stdout.write(type(self).POSITION_INPUT)
        sys.stdout.write(type(self).COLOR_INPUT)
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

def console():

   # the reason of using it "with" is to get back the default coursor color at the end
   with ConsolePrala("base", 'hungarian', 'swedish') as cp:
      while True:
         cp.round()

if __name__ == "__main__":
    console()
