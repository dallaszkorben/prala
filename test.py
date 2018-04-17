#!env/bin/python
from prala.test_core import TestWordCycle
from prala.test_console import TestConsole
import unittest

if __name__ == "__main__":
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestWordCycle)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestConsole)
    unittest.TextTestRunner(verbosity=2).run(suite)