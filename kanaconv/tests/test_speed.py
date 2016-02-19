#!/usr/bin/env python
# coding=utf8
#
# (C) 2015-2016, MIT License

import unittest
import timeit
from math import trunc
from kanaconv.converter import KanaConv
from .assets import tests_freq1000

LOOPS_FEEDBACK = '{loops} loops, best of {attempts}: {time:.5f} secs'
CONV_FEEDBACK = '{conv} conversions, average of {avg:d} usec per conversion'


class TestSpeed(unittest.TestCase):
    '''
    Iterates over the largest test case (the 1000 most frequent lemmas
    on Wikipedia) several times using timeit to get a representative
    indication of the module's conversion speed.

    To run: ./test_kanaconv.py TestSpeed
    '''
    def test_freq1000(self):
        conv = KanaConv()

        def perform_test():
            '''
            Runs the actual test. Isolated function for use with timeit.
            '''
            for test in tests_freq1000:
                conv.to_romaji(test[0])

        attempts = 5
        loops = 15
        time_result = min(timeit.Timer(perform_test).repeat(attempts, loops))
        conversions = len(tests_freq1000) * loops
        print(LOOPS_FEEDBACK.format(
            loops=loops,
            attempts=attempts,
            time=time_result
        ))
        print(CONV_FEEDBACK.format(
            conv=conversions,
            avg=trunc((time_result / conversions) * 1000000)
        ))

if __name__ == '__main__':
    unittest.main()
