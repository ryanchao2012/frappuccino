import unittest


def run_testsuite(cls):
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(cls))
    runner = unittest.TextTestRunner()
    return runner.run(suite)