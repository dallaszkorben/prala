#!env/bin/python
from prala.test_core_01 import TestWordCycleFunctions
from prala.test_core_02 import TestWordCycleInit
from prala.test_console import TestConsole
import unittest


if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordCycleFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordCycleInit)
    unittest.TextTestRunner(verbosity=2).run(suite)
