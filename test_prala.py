import unittest
from prala import WordCycle
import itertools
from collections import Counter

class TestWordCycle(unittest.TestCase):

    # Runs at the beginning of the test suit
    @classmethod
    def setUpClass(cls): 
        pass

    #Runs before every testcase
    def setUp(self): 
        pass

    def test_get_points( self ):
        myWordCycle=WordCycle()        
        
        stat_list=[list(i) for i in list(itertools.product([0,1], repeat=3))]
        expected_list=[7,3,5,2,6,3,4,1]
        # run with all statuses -> result zipped with the expected valus -> pairs substracted from each other -> sum -> it must be 0
        self.assertEqual( sum( [ j[0]-j[1] for j in zip( [myWordCycle.get_points(i) for i in stat_list], expected_list) ] ), 0 )

    def test_get_random_word_equal_chances_all( self ):
        myWordCycle=WordCycle()        
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,0,0],   # no good answer
        }

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 1.0, delta=0.08)

    def test_get_random_word_equal_chances_some( self ):
        myWordCycle=WordCycle()        
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,1,0],   # there was 1 good answer
        }

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 0.0, delta=0.0)

    def test_get_random_word_wighted_chance( self ):
        myWordCycle=WordCycle()        
        
        #stat_list=[["1", list(i)] for i in list(itertools.product([0,1], repeat=3))]
       
        stat_list={
            "a": [1,1,1],   # 1 point  (weight)
            "b": [0,0,1],   # 3 points (weight)
        }

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 3.0, delta=0.08)

    #Runs after every testcase - anyway	
    def tearDown(self): 
        pass

    # Runs at the end of the test suit
    @classmethod
    def tearDownClass(cls): 
        pass

if __name__ == "__main__":
	unittest.main()