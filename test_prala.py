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
        """
        Tests if a list of statistics have back the right points.
        The list and the expected points are the following:
            [0, 0, 0]   -> 7
            [0, 0, 1]   -> 3
            [0, 1, 0]   -> 5
            [0, 1, 1]   -> 2
            [1, 0, 0]   -> 6
            [1, 0, 1]   -> 3
            [1, 1, 0]   -> 4
            [1, 1, 1]   -> 1
        """
        myWordCycle=WordCycle()        
        
        stat_list=[list(i) for i in list(itertools.product([0,1], repeat=3))]
        expected_list=[7,3,5,2,6,3,4,1]
        # run with all statuses -> result zipped with the expected valus -> pairs substracted from each other -> sum -> it must be 0
        self.assertEqual( sum( [ j[0]-j[1] for j in zip( [myWordCycle.get_points(i) for i in stat_list], expected_list) ] ), 0 )

    def test_get_random_word_equal_chances_all( self ):
        """
        Tests if there is about 50%/50% chance to get the words
        which had not got good answer yet
        """
        myWordCycle=WordCycle()        
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,0,0],   # no good answer
        } 

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 1.0, delta=0.08)

    def test_get_random_word_equal_chances_some( self ):
        """
        Tests if there is 0.0% chance to get the word
        which had got a good answer
        """

        myWordCycle=WordCycle()        
        
        stat_list={
            "a": [0,0,0],   # no good answer
            "b": [0,1,0],   # there was 1 good answer
        }

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 0.0, delta=0.0)

    def test_get_random_word_wighted_chance( self ):
        """
        Tests if the chance to get the words
        are proportional to the point (weight) what they have.
        """

        myWordCycle=WordCycle()        
        
        stat_list={
            "a": [1,1,1],   # 1 point  (weight)
            "b": [0,0,1],   # 3 points (weight)
        }

        result=Counter( [myWordCycle.get_random_word(stat_list) for i in range(40000)] )
        self.assertAlmostEqual( result["b"] / result["a"], 3.0, delta=0.08)

    def test_get_next_no_good_answer( self ):
        """
        Tests if there is about same chance to get the words
        which had not got good answer yet
        """
        myWordCycle=WordCyrcleMostHaveNoGoodAnswer()
        loop=300000
        result=Counter([myWordCycle.get_next()[1] for i in range(loop)])
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
        myWordCycle=WordCyrcleAllHaveGoodAnswer()
        loop=40000
        result=Counter([myWordCycle.get_next()[1] for i in range(loop)])
        self.assertAlmostEqual(result['aaa']/loop, 1/10, delta=0.01)
        self.assertAlmostEqual(result['bbb']/loop, 2/10, delta=0.01)
        self.assertAlmostEqual(result['ccc']/loop, 3/10, delta=0.01)
        self.assertAlmostEqual(result['ddd']/loop, 4/10, delta=0.01)
        

    #Runs after every testcase - anyway	
    def tearDown(self): 
        pass

    # Runs at the end of the test suit
    @classmethod
    def tearDownClass(cls): 
        pass

class WordCyrcleMostHaveNoGoodAnswer(WordCycle):
    def __init__(self):
        self.recent_stat={
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

class WordCyrcleAllHaveGoodAnswer(WordCycle):
    def __init__(self):
        self.recent_stat={
            "1":[1,1,1],    # 1 point => 1/10 probability
            "2":[0,1,1],    # 2 points => 2/10 probability
            "3":[0,0,1],    # 3 points => 3/10 probability
            "4":[1,1,0],    # 4 points => 4/10 probability
        }

        self.word_dict={
            "1":('v', 'aaa', ['AAA']),
            "2":('v', 'bbb', ['BBB']),
            "3":('v', 'ccc', ['CCC']),
            "4":('v', 'ddd', ['DDD'])
        }


if __name__ == "__main__":
	unittest.main()