# coding=utf8
#
# (C) 2015-2016, MIT License

import unittest
from kanaconv.converter import KanaConv

from .assets import (
    tests_apostrophe, tests_preprocessing, tests_rare_exc, tests_word_border,
    tests_long_vowels, tests_xvowels, tests_xtsu_chi, tests_freq1000
)


class TestConverter(unittest.TestCase):
    '''
    Test case for the KanaConv class that covers all implemented
    conversion rules and checks whether all rare edge cases are
    correctly handled.

    Every check is a simple string comparison between what the output
    is expected to be, and what the output actually is.

    Run this using ./setup.py test
    '''
    def setUp(self):
        '''
        Initialize the KanaConverter.
        '''
        self.conv = KanaConv()

    def _run_tests(self, tests):
        '''
        Runs a series of assertEqual() tests.
        '''
        for test in tests:
            output = self.conv.to_romaji(test[0])
            with self.subTest(word=test[0]):
                self.assertEqual(output, test[1])

    def test_apostrophe(self):
        self._run_tests(tests_apostrophe)

    def test_word_border(self):
        self._run_tests(tests_word_border)

    def test_long_vowels(self):
        self._run_tests(tests_long_vowels)

    def test_xvowels(self):
        self._run_tests(tests_xvowels)

    def test_xtsu_chi(self):
        self._run_tests(tests_xtsu_chi)

    def test_rare_exc(self):
        self._run_tests(tests_rare_exc)

    def test_preprocessing(self):
        self._run_tests(tests_preprocessing)

    def test_freq1000(self):
        self._run_tests(tests_freq1000)


if __name__ == '__main__':
    unittest.main()
