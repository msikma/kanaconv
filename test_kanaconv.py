#!/usr/bin/env python
# coding=utf8
#
# (C) 2015, MIT License

from kanaconv.converter import KanaConv
import unittest


# Tests many general cases.
tests_miscellaneous = [
    (u'メロディー', u'merodī'),
    (u'みっつ', u'mittsu'),
    # A long vowel marker that appears before any character it could
    # affect should be ignored.
    (u'ーテー', u'tē'),
]

# Tests whether the 'n' before labial consonants/vowels/y is converted
# to 'n\'' (including apostrophe).
tests_apostrophe = [
    (u'しんよう', u'shin\'yō'),
    (u'かんい', u'kan\'i')
]

# Tests whether the word border character, '|', correctly
# prevents rōmaji long vowels from showing up.
tests_word_border = [
    (u'ぬれ|えん', u'nureen'),
    (u'ぬれえん', u'nurēn'),  # in case the separator is missing
    (u'こ|おどり', u'koodori'),
    (u'まよ|う', u'mayou')
]

# Tests hiragana and katakana long vowels.
tests_long_vowels = [
    (u'がっこう', u'gakkō'),
    (u'きいろ', u'kiiro'),  # not kīro; i + i does not yield a long vowel
    (u'セーラー', u'sērā'),
    (u'おねえさん', u'onēsan'),
    (u'こおり', u'kōri'),
    (u'スーパーマン', u'sūpāman'),
    (u'とうきょう', u'tōkyō'),
    (u'パーティー', u'pātī'),
    (u'く|う', u'kuu')  # the last 'u' is not converted to 'ū'
]

# Tests hiragana and katakana small vowels, including unusual
# combinations.
tests_xvowels = [
    (u'しょ', u'sho'),
    # Some unusual combinations:
    (u'ワァ', u'wā'),
    (u'ワァィ', u'wāi')
]

# Tests the usage of a small ツ in front of チ.
tests_xtsu_chi = [
    (u'まっちゃ', u'matcha'),
    (u'ぼっちゃん', u'botchan'),
    (u'ボッチャン', u'botchan'),
    (u'ボっチゃン', u'botchan'),  # mixture of hiragana and katakana
    (u'こっち', u'kotchi')
]

class TestKanaConv(unittest.TestCase):
    '''
    Test case for the KanaConverter class that covers all implemented
    conversion rules and checks whether all rare edge cases are
    correctly handled.

    Every check is a simple string comparison between what the output
    is expected to be, and what the output actually is.
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
            self.assertEqual(output, test[1])

    def test_miscellaneous(self):
        self._run_tests(tests_miscellaneous)

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

if __name__ == '__main__':
    unittest.main()
