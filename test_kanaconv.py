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

# Tests whether we're correctly running pre-processing transformations.
# These take place before we run the regular transliteration algorithm.
tests_preprocessing = [
    # transform full-width rōmaji to standard Latin characters
    (u'オールＡ', u'ōruA'),
    (u'ＡＢＣＤＥＦＧＨＩ', u'ABCDEFGHI'),
    (u'ＪＫＬＭＮＯＰＱＲ', u'JKLMNOPQR'),
    (u'ＳＴＵＶＷＸＹＺ１', u'STUVWXYZ1'),
    (u'２３４５６７８９０', u'234567890'),
    (u'ａｂｃｄｅｆｇｈｉ', u'abcdefghi'),
    (u'ｊｋｌｍｎｏｐｑｒ', u'jklmnopqr'),
    (u'ｓｔｕｖｗｘｙｚ', u'stuvwxyz'),
    # ヿ is a ligature for コト
    (u'ヿ', u'koto'),
    # unusual (non-existent?) combination but theoretically possible
    (u'ヿー', u'kotō'),
    # ゟ is a ligature for より
    (u'えきゟ', u'ekiyori'),
    # check the usage of the archaic repeater characters
    (u'さゝき', u'sasaki'),
    (u'あひゞき', u'ahibiki'),
    # check the usage of the ゠ character (for dashes in proper names)
    (u'ラッセル゠アインシュタイン', u'rasseru-einshutain'),
    # check whether combining (han)dakuten characters are converted
    (u'か\u3099か', u'gaka'),
    (u'は\u309aは', u'paha')
]

# Tests for rare and (mostly) obsolete characters.
tests_rare = [
    # ウェ is preferred for 'we'
    (u'ウェスト', u'wesuto'),
    # ウィ is 'wi', and full-width rōmaji is transliterated into latin
    (u'ウィンドウズＸＰ', u'windouzuXP'),
    # ヴェ is used for 've'
    (u'アヴェニュー', u'avenyū'),
    # ヹ is sometimes (very rarely) used instead of ヴェ
    (u'アヹ', u'ave'),
    # ゑ is technically 'we', but is used as though it's 'e'
    (u'ゑびす', u'ebisu'),
    # ヱ is the katakana version of ゑ, and sometimes it's 'ye'
    (u'ヱビス', u'ebisu'),
    # ヰ is 'wi', for which ウイ or ウィ is now preferred
    (u'スヰーデン', u'suwīden'),
    # rare version of ウイスキー
    (u'ヰスキー', u'wisukī'),
    # archaic ligature for 'koto'
    (u'スルヿ', u'surukoto'),
    # small 'ka' and 'ke', though the katakana ヶ is pronounced as 'ka'
    (u'ゕーゖーヵーヶー', u'kākēkākā')
]

# Tests whether the word border character, '|', correctly
# prevents rōmaji long vowels from showing up.
tests_word_border = [
    (u'ぬれ|えん', u'nureen'),
    # in case the separator is missing
    (u'ぬれえん', u'nurēn'),
    (u'こ|おどり', u'koodori'),
    (u'まよ|う', u'mayou')
]

# Tests hiragana and katakana long vowels.
tests_long_vowels = [
    (u'がっこう', u'gakkō'),
    # not kīro; i + i does not yield a long vowel
    (u'きいろ', u'kiiro'),
    (u'セーラー', u'sērā'),
    (u'おねえさん', u'onēsan'),
    (u'こおり', u'kōri'),
    (u'スーパーマン', u'sūpāman'),
    (u'とうきょう', u'tōkyō'),
    (u'パーティー', u'pātī'),
    # the last 'u' is not converted to 'ū'
    (u'く|う', u'kuu'),
    (u'シーチキン', u'shīchikin')
]

# Tests hiragana and katakana small vowels, including unusual
# combinations.
tests_xvowels = [
    (u'しょ', u'sho'),
    # チェ is used for 'che', which chiefly katakana
    (u'チェコきょうわこく', u'chekokyouwakoku'),
    # some unusual combinations:
    (u'ワァ', u'wā'),
    (u'ワァィ', u'wāi')
]

# Tests the usage of a small ッ in front of チ and ツ.
tests_xtsu_chi = [
    (u'まっちゃ', u'matcha'),
    (u'ぼっちゃん', u'botchan'),
    (u'ボッチャン', u'botchan'),
    # mixture of hiragana and katakana
    (u'ボっチゃン', u'botchan'),
    (u'こっち', u'kotchi')
]

class TestKanaConv(unittest.TestCase):
    '''
    Test case for the KanaConv class that covers all implemented
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

    def test_rare(self):
        self._run_tests(tests_rare)

    def test_preprocessing(self):
        self._run_tests(tests_preprocessing)

if __name__ == '__main__':
    unittest.main()
