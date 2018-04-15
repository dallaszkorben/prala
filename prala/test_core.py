import unittest
from core import FilteredDictionary
from core import Record

import itertools
from collections import Counter
#from pathlib import Path
import os

class TestWordCycle(unittest.TestCase):
    BASE_NAME="testfile"
    DICT_FILE=BASE_NAME + "." + FilteredDictionary.DICT_EXT

    # Runs at the beginning of the test suit
    @classmethod
    def setUpClass(cls):
        content={
            "1":('v', 'aaa', ['Abc', 'Adef', 'Aghij', 'Aklmnopq', 'A']),
            "2":('a', 'bbb', ['Bcd', 'Befg', 'Bhijk']),
            "3":('n', 'ccc', ['Cde']),
            "4":('b', 'ddd', ['Def'])
        }

        with open( TestWordCycle.DICT_FILE, "w" ) as f:
            print(*[FilteredDictionary.RECORD_SPLITTER.join([k]+[v[0]]+[v[1]]+[", ".join(v[2])]) for k, v in content.items()], sep='\n', file=f)

    #Runs before every testcase
    def setUp(self): 
        pass
        #self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish') 

    def test_get_points( self ):
        """
        Tests if a list of statistics have back the right points.
        The list and the expected points are the following:
            [0, 0, 0]   -> 7
            [0, 0, 1]   -> 2
            [0, 1, 0]   -> 4
            [0, 1, 1]   -> 1
            [1, 0, 0]   -> 5
            [1, 0, 1]   -> 2
            [1, 1, 0]   -> 3
            [1, 1, 1]   -> 1
        """
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish') 

        stat_list=[list(i) for i in list(itertools.product([0,1], repeat=3))]
        expected_list=[7,2,4,1,5,2,3,1]
        # run with all statuses -> result zipped with the expected valus -> pairs substracted from each other -> sum -> it must be 0
        self.assertEqual( sum( [ j[0]-j[1] for j in zip( [self.myFilteredDictionary.get_points(i) for i in stat_list], expected_list) ] ), 0 )

    def test_get_random_id_equal_chances_all( self ):
        """
        Tests if there is about 50%/50% chance to get the words
        which had not got good answer yet
        """
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish') 
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,0,0],   # no good answer
        } 

        result=Counter( [self.myFilteredDictionary.get_random_id(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 1.0, delta=0.08)

    def test_get_random_id_equal_chances_some( self ):
        """
        Tests if there is 0.0% chance to get the word
        which had got a good answer
        """

        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish') 
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,1,0],   # there was 1 good answer
        }

        result=Counter( [self.myFilteredDictionary.get_random_id(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 0.0, delta=0.0)

    def test_get_random_id_wighted_chance( self ):
        """
        Tests if the chance to get the words
        are proportional to the point (weight) what they have.
        """

        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish') 
        
        stat_list={
            "a": [1,1,1],   # 1 point  (weight)
            "b": [0,0,1],   # 2 points (weight)
        }

        result=Counter( [self.myFilteredDictionary.get_random_id(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 2.0, delta=0.08)

    def test_get_next_random_record_only_one_good_answer( self ):
        """
        Tests if there is about same chance to get the words
        which had not got good answer yet
        """
        
        myFilteredDictionary=WordCyrcleMostHaveNoGoodAnswer()
        loop=300000
        result=Counter([myFilteredDictionary.get_next_random_record().base_word for i in range(loop)])
        self.assertAlmostEqual( loop/3, result['aaa'], delta=600)
        self.assertAlmostEqual( loop/3, result['bbb'], delta=600)
        self.assertAlmostEqual( 0.0, result['ccc'], delta=0)
        self.assertAlmostEqual( loop/3, result['ddd'], delta=600)

    def test_get_next_has_good_answer( self ):
        """
        Tests if the chance to get the words
        are proportional to the point (weight) what they have.
        It means: 10%/20%/30%/40% in sequence
        """
        myFilteredDictionary=WordCyrcleAllHaveGoodAnswer()
        loop=40000
        result=Counter([myFilteredDictionary.get_next_random_record().base_word for i in range(loop)])
        self.assertAlmostEqual(result['aaa']/loop, 1/10, delta=0.01)
        self.assertAlmostEqual(result['bbb']/loop, 2/10, delta=0.01)
        self.assertAlmostEqual(result['ccc']/loop, 3/10, delta=0.01)
        self.assertAlmostEqual(result['ddd']/loop, 4/10, delta=0.01)
    
    def test_check_answer_true( self ):
        """
        Checks if I get True return and empty differece list 
        when all answer equals to the base
        """
        
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        
        answer=['Abc', 'Adef', 'Aghij', 'Aklmnopq', 'A']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertTrue(result[0])
        self.assertEqual(sum([1 for i in result[1] if len(i) != 0]), 0 )
 
    def test_check_answer_false_shorter_list( self ):
        """
        Checks if I get False return and the corresponding difference list
        when some answers are different to the bases
        """

        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        
        answer=['Adc', 'Adef', 'Adhlj', 'Aklmnopq']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0],[1])
        self.assertEqual(result[1][1],[])
        self.assertEqual(result[1][2],[1,3])
        self.assertEqual(result[1][4],[0])

    def test_check_answer_false_longer_list( self ):
        """
        Checks if I get False return and the corresponding difference list
        when the answer list is longer than the base
        """

        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        
        answer=['Abc', 'Adef', 'Aghij', 'Aklmnopq', 'A', 'Abcd']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0],[])
        self.assertEqual(result[1][1],[])
        self.assertEqual(result[1][2],[])
        self.assertEqual(result[1][3],[])
        self.assertEqual(result[1][4],[])
        self.assertEqual(result[1][5],[0, 1, 2, 3])

    def test_check_answer_false_shorter_answer( self ):
        """
        Checks if I get False return and the corresponding difference list
        when the answer list has at least one shorter answer than the base
        """
        
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        
        answer=['Abc', 'Adef', 'Agh', 'Aklmnopq', 'A']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0],[])
        self.assertEqual(result[1][1],[])
        self.assertEqual(result[1][2],[3,4])
        self.assertEqual(result[1][3],[])
        self.assertEqual(result[1][4],[])

    def test_check_answer_false_longer_answer( self ):
        """
        Checks if I get False return and the corresponding difference list
        when the answer list has at least one longer answer than the base
        """        
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v')
        answer=['Abc', 'Adef', 'Aghijkl', 'Aklmnopq', 'A']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0],[])
        self.assertEqual(result[1][1],[])
        self.assertEqual(result[1][2],[5,6])
        self.assertEqual(result[1][3],[])
        self.assertEqual(result[1][4],[])

    def test_check_answer_false_empty_answer( self ):
        """
        Checks if I get False return and the corresponding difference list
        when the answer list has at least one empty answer
        """        
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v')
        answer=['Abc', '', 'Aghij', 'Aklmnopq', 'A']
        result=self.myFilteredDictionary.get_next_random_record().check_answer(answer)
        self.assertFalse(result[0])
        self.assertEqual(result[1][0],[])
        self.assertEqual(result[1][1],[0,1,2,3])
        self.assertEqual(result[1][2],[])
        self.assertEqual(result[1][3],[])
        self.assertEqual(result[1][4],[])

    def test_add_result_to_stat( self ):
        """
        """
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        
        record=self.myFilteredDictionary.get_next_random_record()
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)
        self.assertEqual( record.get_recent_stat(), [1,0,1] )
       
    def test_(self):
 
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='') 
        
        record=self.myFilteredDictionary.get_next_random_record()
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)

        record=self.myFilteredDictionary.get_next_random_record()
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)

        record=self.myFilteredDictionary.get_next_random_record()
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)

        record=self.myFilteredDictionary.get_next_random_record()
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, False)
        self.myFilteredDictionary.add_result_to_stat(record.word_id, True)

        res_stat=self.myFilteredDictionary.get_recent_stat_list()
        self.assertEqual(res_stat[0], 13)
        self.assertEqual(res_stat[1], 5)
        self.assertEqual(res_stat[2], 4)

    def _test_say_out_base(self):
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        self.myFilteredDictionary.get_next_random_record().say_out_base()

    def _test_say_out_learning(self):
        self.myFilteredDictionary=FilteredDictionary(TestWordCycle.BASE_NAME, 'hungarian', 'swedish', part_of_speach_filter='v') 
        self.myFilteredDictionary.get_next_random_record().say_out_learning()

    #Runs after every testcase - anyway	
    def tearDown(self): 
        pass

    # Runs at the end of the test suit
    @classmethod
    def tearDownClass(cls): 
        os.remove(TestWordCycle.DICT_FILE)
        os.remove(TestWordCycle.BASE_NAME+".bak")
        os.remove(TestWordCycle.BASE_NAME+".dat")
        os.remove(TestWordCycle.BASE_NAME+".dir")

class WordCyrcleMostHaveNoGoodAnswer(FilteredDictionary):
    def __init__(self):
        self.base_language="hungarian"
        self.learning_language="swedish"
        self.recent_stat_list={
            "1":[0,0,0],
            "2":[0,0,0],
            "3":[0,1,0],
            "4":[0,0,0],
        }
        self.word_dict={
            "1":('v', 'aaa', ['AAA']),
            "2":('v', 'bbb', ['BBB']),
            "3":('v', 'ccc', ['CCC']),
            "4":('v', 'ddd', ['DDD'])
        }

class WordCyrcleAllHaveGoodAnswer(FilteredDictionary):
    
    def __init__(self):
        self.base_language="hungarian"
        self.learning_language="swedish"
        self.recent_stat_list={
            "1":[1,1,1],    # 1 point => 1/10 probability
            "2":[1,0,1],    # 2 points => 2/10 probability
            "3":[1,1,0],    # 3 points => 3/10 probability
            "4":[0,1,0],    # 4 points => 4/10 probability
        }
        self.word_dict={
            "1":('v', 'aaa', ['AAA']),
            "2":('v', 'bbb', ['BBB']),
            "3":('v', 'ccc', ['CCC']),
            "4":('v', 'ddd', ['DDD'])
        }

(7, [0, 0, 0]), 
(2, [0, 0, 1]), 
(4, [0, 1, 0]), 
(1, [0, 1, 1]), 
(5, [1, 0, 0]), 
(2, [1, 0, 1]), 
(3, [1, 1, 0]), 
(1, [1, 1, 1])

if __name__ == "__main__":
	unittest.main()