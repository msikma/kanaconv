# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
Finite state machine that converts hiragana and katakana strings to rōmaji
according to Modified Hepburn transliteration rules.

Only kana and romaji is usable; kanji can't be used as input.

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

The theoretical combinations yi, ye and wu don't exist, nor does the
repeater mark with handakuten.
'''
from kanaconv.utils import kana_romaji_lt
from kanaconv.charsets import romaji, katakana, hiragana, lvmarker


# Lookup table for consonant-vowel (cv) kana and their rōmaji data.
cvs_romaji = romaji['set_cvs']
cvs_katakana = katakana['set_cvs']
cvs_hiragana = hiragana['set_cvs']
cv_lt = kana_romaji_lt(cvs_romaji, cvs_katakana, cvs_hiragana)

# Lookup table for vowel kana.
vowels_romaji = romaji['set_vowels']
vowels_katakana = katakana['set_vowels']
vowels_hiragana = hiragana['set_vowels']
vowel_lt = kana_romaji_lt(vowels_romaji, vowels_katakana, vowels_hiragana)

# Lookup table for small vowel kana.
xvowels_romaji = romaji['set_xvowels']
xvowels_katakana = katakana['set_xvowels']
xvowels_hiragana = hiragana['set_xvowels']
xvowel_lt = kana_romaji_lt(xvowels_romaji, xvowels_katakana, xvowels_hiragana)

# We use sets to be able to do quick lookups.
cvs = set(cv_lt)
vowels = set(vowel_lt)
xvowels = set(xvowel_lt)
geminates = {katakana['geminate'], hiragana['geminate']}

# The machine's constants.
EMPTY_BUFFER = 10
END_CHAR = 11

# Two special characters that change the machine's behavior.
WORD_SEPARATOR = '|'      # word boundary, e.g. 仔馬 = こ|うま = kouma, not kōma.
PARTICLE_INDICATOR = '.'  # indicates a particle, e.g. わたし.は = watashi wa.


class KanaConverter(object):
    '''
    The main converter class. After initialization, use to_romaji()
    to convert a kana string to rōmaji.
    '''
    def __init__(self):
        '''
        Initializes the variables we'll use in the state machine.

        Also see the set_state() function.
        '''
        # The character stack, containing the characters of the romaji output.
        self.stack = []

        # Number of long vowel markers in the state.
        self.lvmarker_count = 0

        # Number of geminate markers in the state.
        self.geminate_count = 0

        # The currently active small vowel character.
        self.active_xvowel = None
        self.active_xvowel_info = None

        # The currently active character.
        self.active_char = None
        self.active_char_info = None

        self.empty_stack()
        self.set_state(EMPTY_BUFFER)

    def empty_stack(self):
        self.stack = []

    def flush_char(self):
        if self.active_char is None:
            return

        char_info = self.active_char_info
        char = char_info[0]
        xv = self.active_xvowel_info
        gem = self.geminate_count
        lvm = self.lvmarker_count

        # If no modifiers are active (geminate marker, small vowel marker,
        # etc.) then just the currently active character is flushed.
        if xv is None and gem == 0 and lvm == 0:
            self.stack.append(char)
            self.set_state(EMPTY_BUFFER)
            return

        # Deconstruct the info object for clarity.
        char_gem_cons = char_info[1]  # the extra geminate consonant
        char_cons = char_info[2]      # the consonant part of the character
        char_mvowel = char_info[3]    # the macron vowel part of the character

        # Determine the geminate consonant part, if any.
        gem_cons = char_gem_cons * gem

        # At this point, we're considering two main factors: the currently
        # active character, and possibly a small vowel character if one is set.
        # For example, if the active character is テ and a small vowel ィ
        # is set, the result is 'ti'. If no small vowel is set, just
        # plain 'te' comes out.
        #
        # Aside from this choice, we're also considering the number of active
        # long vowel markers, which repeats the vowel part. If there's
        # at least one long vowel marker, we also use a macron vowel
        # rather than the regular one, e.g. 'ī' instead of 'i'.

        # If there's an active small vowel, integrate it with the consonant
        # of the active character.
        if xv is not None:
            # Combine the consonant of the character with the small vowel.
            # Use a macron vowel if there's a long vowel marker,
            # else use the regular vowel.
            vowel = xv[1] * lvm if lvm > 0 else xv[0]
            self.stack.append(gem_cons + char_cons + vowel)
        else:
            # Add either a character with macron if needed, or just
            # the plain character.
            char_main = char_cons + char_mvowel * lvm if lvm > 0 else char
            self.stack.append(gem_cons + char_main)

        self.set_state(EMPTY_BUFFER)

    def set_state(self, state):
        if state is EMPTY_BUFFER:
            self.lvmarker_count = 0
            self.geminate_count = 0
            self.active_xvowel = None
            self.active_xvowel_info = None
            self.active_char = None
            self.active_char_info = None

    def set_char(self, char):
        self.active_char = char
        self.active_char_info = cv_lt[char]

    def set_xvowel(self, xvowel):
        self.active_xvowel = xvowel
        self.active_xvowel_info = xvowel_lt[xvowel]

    def inc_geminate(self):
        self.geminate_count += 1

    def inc_lvmarker(self):
        self.lvmarker_count += 1

    def flush_stack(self):
        output = ''.join(self.stack)
        self.set_state(EMPTY_BUFFER)
        self.empty_stack()
        return output

    def to_romaji(self, input):
        chars = list(input)
        chars.append(END_CHAR)
        for char in chars:
            print(char)
            if char in cvs:
                self.flush_char()
                self.set_char(char)
                continue

            if char in vowels:
                print('vowel')
                pass
                continue

            if char in xvowels:
                self.set_xvowel(char)
                continue

            if char in geminates:
                # fixme: set geminate count to 0 in else?
                self.flush_char()
                self.inc_geminate()
                continue

            if char == lvmarker:
                self.inc_lvmarker()
                continue

            if char is END_CHAR:
                self.flush_char()
                continue

        return self.flush_stack()
