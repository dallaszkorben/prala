import unittest
from prala import WordCycle
import itertools

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
        #stat_list=[["1", list(i)] for i in list(itertools.product([0,1], repeat=3))]
        stat_list=[list(i) for i in list(itertools.product([0,1], repeat=3))]
        result_list=[7,3,5,2,6,3,4,1]
        self.assertEqual( sum( [ j[0]-j[1] for j in zip( [myWordCycle.get_points(i) for i in stat_list], result_list) ] ), 0 )
                
    #Runs after every testcase - anyway	
    def tearDown(self): 
        pass

    # Runs at the end of the test suit
    @classmethod
    def tearDownClass(cls): 
        pass

if __name__ == "__main__":
	unittest.main()