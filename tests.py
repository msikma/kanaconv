# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

from kanaconv.converter import KanaConverter
import unittest


# Initialize the KanaConverter.
conv = KanaConverter()


class TestKanaConverter(unittest.TestCase):
    '''
    Test case for the KanaConverter class that covers all implemented
    conversion rules and checks whether all rare edge cases are
    correctly handled.

    Every check is a simple string comparison between what the output
    is expected to be, and what the output actually is.
    '''
    def _run_tests(self, tests):
        '''
        Runs a series of assertEqual() tests.
        '''
        for test in tests:
            input = test[0]
            expected = test[1]
            output = conv.to_romaji(input)
            self.assertEqual(output, expected)

    def test_miscellaneous(self):
        '''
        Tests many general cases.
        '''
        # todo: add many more
        tests = [
            (u'メロディー', u'merodī'),
            (u'みっつ', u'mittsu')
        ]
        self._run_tests(tests)

    def test_apostrophe(self):
        '''
        Tests whether the 'n' before labial consonants/vowels/y is converted
        to 'n\'' (including apostrophe).
        '''
        # todo: fix description
        tests = [
            (u'しんよう', u'shin\'yō'),
            (u'かんい', u'kan\'i')
        ]
        self._run_tests(tests)

    def test_word_separator(self):
        '''
        Tests whether the word separator character, '|', correctly
        prevents rōmaji long vowels from showing up.
        '''
        tests = [
            (u'ぬれ|えん', u'nureen'),
            (u'ぬれえん', u'nurēn'),  # in case the separator is missing
            (u'こ|おどり', u'koodori'),
            (u'まよ|う', u'mayou')
        ]
        self._run_tests(tests)

    def test_long_vowels(self):
        '''
        Tests hiragana and katakana long vowels.
        '''
        tests = [
            (u'がっこう', u'gakkō'),
            (u'セーラー', u'sērā'),
            (u'おねえさん', u'onēsan'),
            (u'こおり', u'kōri'),
            (u'スーパーマン', u'sūpāman'),
            (u'とうきょう', u'tōkyō'),
            (u'パーティー', u'pātī'),
            (u'食う', u'kuu')  # the last 'u' is not converted to 'ū'.
        ]
        self._run_tests(tests)

    def test_xtsu_chi(self):
        '''
        Tests the usage of a small ツ in front of チ.
        '''
        tests = [
            (u'まっちゃ', u'matcha'),
            (u'ぼっちゃん', u'botchan'),
            (u'ボッチャン', u'botchan'),
            (u'ボっチゃン', u'botchan'),  # mixture of hiragana and katakana
            (u'こっち', u'kotchi')
        ]
        self._run_tests(tests)

if __name__ == '__main__':
    unittest.main()
