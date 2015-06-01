# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
Converts hiragana and katakana strings to rōmaji according to Modified Hepburn
transliteration rules.

Only kana and romaji is usable; kanji can't be used as input for this class.

Aside from the usual kana, the following are supported:

   * The wi/we kana characters（ゐゑ・ヰヱ）
   * The repeater characters（ゝゞヽヾ）
   * The koto ligature（ヿ）
   * Small ka (ゕ; U+3095, and ヵ; U+30F5)
   * Small ke (ゖ; U+3096, and ヶ; U+30F6)

Conversely, the following characters and features are not supported,
with no plans to support them in the future:

   * Half width katakana (U+FF65 - U+FF9F)
   * Enclosed katakana (U+32D0 - U+32FE)
   * Katakana phonetic extensions (U+31F0 - U+31FF)
   * Historical kana supplement (U+1B000, U+1B001)
   * "Here" sign (🈁; U+1F201)
   * "Service" sign (🈂; U+1F202)
   * "Data" sign (🈓; U+1F213)
   * Rare typographical symbols
   * Vertical-only symbols

Developers who don't speak Japanese should know that the theoretical
combinations yi, ye and wu don't exist, nor does the repeater mark with
handakuten.
'''
import re
from kanaconv import xkana
from kanaconv import romaji
from kanaconv.constants import punctuation, hiragana_romaji, katakana_romaji

class KanaConverter(object):
    def __init__(self):
        # The main lookup tables that we'll use.
        romaji = [char[0] for char in hiragana_romaji]
        hiragana = [char[1] for char in hiragana_romaji]
        katakana = [char[1] for char in katakana_romaji]

        # Initialize the regexes we use for making string replacements.
        self.punct_re = re.compile(
            '(%s)' % '|'.join(map(re.escape, punctuation.keys())),
            re.UNICODE
        )

    def to_romaji(self, string, safe_mode=False):
        '''
        Converts a string from hiragana or katakana to rōmaji.
        '''
        # todo: normalize the dakuten
        string = xkana.normalize_dakuten(string)

        # To make it easier to process the string, we'll remove the
        # long vowel marker even if it's a katakana string.
        string = xkana.normalize_lvm(string, xkana.HIRAGANA)

        # Perform the actual string replacements for the kana.
        for char in hiragana_romaji:
            # todo: add a check here to see if char[1] is in the string
            # as it might be faster
            string = string.replace(char[1], char[0])

        for char in katakana_romaji:
            string = string.replace(char[1], char[0])

        # Convert punctuation.
        string = xkana.replace_punctuation(string)

        # Add macron characters. E.g. change 'raamen' to 'rāmen'.
        string = romaji.add_macrons(string)

        return string

    def punct_sub(self, string):
        '''
        Fast fixed dictionary substitution function.
        Original by Claudiu <http://stackoverflow.com/a/1919123/3553425>.
        '''
        self.punct_re.sub(lambda x: punctuation[x.string[x.start():x.end()]],
                          string)
