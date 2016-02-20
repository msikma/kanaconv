# coding=utf8
#
# (C) 2015-2016, MIT License

import sys
import unittest
from kanaconv.converter import KanaConv
from kanaconv.constants import MACRON_STYLE, CIRCUMFLEX_STYLE

from .assets import (
    tests_apostrophe, tests_preprocessing, tests_rare_exc, tests_word_border,
    tests_long_vowels, tests_xvowels, tests_xtsu_chi, tests_freq1000,
    tests_circumflex, tests_circumflex_uppercase, tests_long_vowels_uppercase
)

# Disables the subtest functionality if we're on Python 2.
PYTHON_2 = sys.version_info < (3, 0)


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

    def _run_tests(self, tests, vowel_style=MACRON_STYLE, uppercase=False):
        '''
        Runs a series of assertEqual() tests.
        '''
        self.conv.set_vowel_style(vowel_style)
        self.conv.set_uppercase(uppercase)

        if not PYTHON_2:
            for test in tests:
                output = self.conv.to_romaji(test[0])
                with self.subTest(word=test[0]):
                    self.assertEqual(output, test[1])
        else:
            for test in tests:
                output = self.conv.to_romaji(test[0])
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

    def test_uppercase(self):
        self._run_tests(tests_long_vowels_uppercase, uppercase=True)

    def test_circumflex(self):
        self._run_tests(tests_circumflex, vowel_style=CIRCUMFLEX_STYLE)
        self._run_tests(
            tests_circumflex_uppercase,
            vowel_style=CIRCUMFLEX_STYLE,
            uppercase=True
        )

if __name__ == '__main__':
    unittest.main()
