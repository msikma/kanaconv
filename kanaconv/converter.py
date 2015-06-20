# coding=utf8
#
# (C) 2015, MIT License

'''
Finite state machine that converts hiragana and katakana strings to rōmaji
according to Modified Hepburn transliteration rules.

Only kana and rōmaji is usable; kanji can't be used as input.

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
from kanaconv.exceptions import (
    InvalidCharacterTypeError, UnexpectedCharacterError)
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
CV = 12
VOWEL = 13
# Strategies for dealing with unknown characters.
UNKNOWN_DELETE = 14
UNKNOWN_RAISE = 15
UNKNOWN_INCLUDE = 16

# The replacement character for impossible geminate marker combinations.
# E.g. っえ becomes -e.
REPL_CHAR = romaji['repl_char']

# The valid character types.
CHAR_TYPES = {CV, VOWEL}

# Two special characters that change the machine's behavior.
WORD_BORDER = '|'      # word boundary, e.g. 子馬 = こ|うま = kouma, not kōma.
PARTICLE_INDICATOR = '.'  # indicates a particle, e.g. わたし.は = watashi wa.


class KanaConv(object):
    '''
    The main converter class. After initialization, use to_romaji()
    to convert a kana string to rōmaji.
    '''
    def __init__(self):
        '''
        Initializes the variables we'll use in the state machine.

        Also see the set_state() function.
        '''
        # What to do with unknown characters; either we delete them,
        # include them in the output, or raise an exception.
        self.unknown_strategy = UNKNOWN_DELETE
        self.unknown_chars = []

        # The character stack, containing the characters of the rōmaji output.
        self.stack = []

        # Number of long vowel markers in the state.
        self.lvmarker_count = 0

        # Number of geminate markers in the state.
        self.geminate_count = 0

        # The currently active rōmaji vowel character.
        self.active_vowel = None
        self.active_vowel_info = None
        self.active_vowel_ro = None

        # The currently active small vowel character.
        self.active_xvowel = None
        self.active_xvowel_info = None

        # The currently active character.
        self.active_char = None
        self.active_char_info = None

        # The type of character; either a consonant-vowel pair or a vowel.
        self.active_char_type = None

        # Reset the machine to a pristine state.
        self.empty_stack()
        self.set_state(EMPTY_BUFFER)

    def set_unknown_strategy(self, behavior):
        '''
        Sets the strategy for dealing with unknown characters.
        '''
        self.unknown_strategy = behavior

    def empty_stack(self):
        '''
        Empties the stack, making the converter ready for the next
        transliteration job.
        '''
        self.stack = []

    def flush_char(self):
        '''
        Appends the rōmaji characters that represent the current state
        of the machine. For example, if the state includes the character
        ト, plus a geminate marker and a long vowel marker, this causes
        the characters "ttō" to be added to the output.
        '''
        if self.active_char is None:
            # Ignore in case there's no active character, only at the very
            # beginning of the conversion process.
            return

        char_info = self.active_char_info
        char_type = self.active_char_type
        char_ro = char_info[0]
        xv = self.active_xvowel_info
        gem = self.geminate_count
        lvm = self.lvmarker_count

        # Check whether we're dealing with a valid char type.
        if not char_type in CHAR_TYPES:
            raise InvalidCharacterTypeError

        # If no modifiers are active (geminate marker, small vowel marker,
        # etc.) then just the currently active character is flushed.
        if xv is None and gem == 0 and lvm == 0:
            self.append_to_stack(char_ro)
            self.set_state(EMPTY_BUFFER)
            return

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

        if char_type == CV:
            # Deconstruct the info object for clarity.
            char_gem_cons = char_info[1]  # the extra geminate consonant
            char_cons = char_info[2]      # the consonant part
            char_lv = char_info[4]        # the long vowel part

            # Determine the geminate consonant part (which can be
            # arbitrarily long).
            gem_cons = char_gem_cons * gem

            # If there's an active small vowel, integrate it with the consonant
            # of the active character.
            if xv is not None:
                # Combine the consonant of the character with the small vowel.
                # Use a macron vowel if there's a long vowel marker,
                # else use the regular vowel.
                vowel = xv[1] * lvm if lvm > 0 else xv[0]
                self.append_to_stack(gem_cons + char_cons + vowel)
            else:
                # Add either a character with macron if needed, or just
                # the plain character.
                char_main = char_cons + char_lv * lvm if lvm > 0 else char_ro
                self.append_to_stack(gem_cons + char_main)

        if char_type == VOWEL:
            char_lv = char_info[1]  # the long vowel part

            if xv is not None:
                xv_ro = xv[1] * lvm if lvm > 0 else xv[0]
                self.append_to_stack(char_ro + xv_ro)
            else:
                vowel_ro = char_lv * lvm if lvm > 0 else char_ro
                self.append_to_stack(vowel_ro)

        # In case we've stumbled upon unknown characters, append them
        # to the output stack as well, in case we want to keep them.
        if self.unknown_strategy == UNKNOWN_INCLUDE and \
           self.unknown_chars is not []:
            self.append_to_stack(self.get_unknown_chars())

        self.set_state(EMPTY_BUFFER)

    def append_to_stack(self, string):
        '''
        Appends a string to the output stack.
        '''
        self.stack.append(string)

    def get_unknown_chars(self):
        return ''.join(self.unknown_chars)

    def add_unknown_char(self, string):
        self.unknown_chars.append(string)

    def set_state(self, state):
        '''
        Resets the machine to a specific base state.
        '''
        if state is EMPTY_BUFFER:
            self.lvmarker_count = 0
            self.geminate_count = 0
            self.active_vowel = None
            self.active_vowel_info = None
            self.active_vowel_ro = None
            self.active_xvowel = None
            self.active_xvowel_info = None
            self.active_char = None
            self.active_char_info = None
            self.active_char_type = None
            self.unknown_chars = []

    def set_char(self, char, type):
        '''
        Sets the currently active character, e.g. ト. We save some information
        about the character as well. active_char_info contains the full
        tuple of rōmaji info, and active_ro_vowel contains e.g. 'o' for ト.

        We also set the character type: either a consonant-vowel pair
        or a vowel. This affects the way the character is flushed later.
        '''
        self.flush_char()

        self.active_char = char
        self.active_char_type = type

        if type == CV:
            self.active_char_info = cv_lt[char]
            self.active_vowel_ro = cv_lt[char][3]

        if type == VOWEL:
            self.active_char_info = vowel_lt[char]
            self.active_vowel_ro = vowel_lt[char][0]

    def set_vowel(self, vowel):
        '''
        Sets the currently active vowel, e.g. ア.

        Vowels act slightly differently from other characters. If one
        succeeds the same vowel (or consonant-vowel pair with the same vowel)
        then it acts like a long vowel marker. E.g. おねえ becomes onē.

        Hence, either we increment the long vowel marker count, or we
        flush the current character and set the active character to this.
        '''
        self.active_vowel = vowel
        self.active_vowel_info = vowel_lt[vowel]

        if self.active_vowel_info[0] == self.active_vowel_ro:
            # Same vowel as the one that's currently active.
            self.inc_lvmarker()
        else:
            # Not the same, so flush the active character and continue.
            self.active_vowel_ro = self.active_vowel_info[0]
            self.flush_char()
            self.set_char(vowel, VOWEL)


    def set_xvowel(self, xvowel):
        '''
        Sets the currently active small vowel, e.g. ァ.
        '''
        self.active_xvowel = xvowel
        self.active_xvowel_info = xvowel_lt[xvowel]

    def inc_geminate(self):
        '''
        Increments the geminate marker count. Unless no active character
        has been set, this causes the current character to be flushed.
        '''
        if self.active_char is not None:
            self.flush_char()
        self.geminate_count += 1

    def inc_lvmarker(self):
        '''
        Increments the long vowel marker count.
        '''
        self.lvmarker_count += 1

    def flush_stack(self):
        '''
        Returns the final output and resets the machine's state.
        '''
        output = ''.join(self.stack)
        self.set_state(EMPTY_BUFFER)
        self.empty_stack()
        return output

    def to_romaji(self, input):
        '''
        Converts kana input to rōmaji and returns the result.
        '''
        chars = list(input)
        chars.append(END_CHAR)
        for char in chars:
            if char in cvs:
                self.set_char(char, CV)
                continue

            if char in vowels:
                self.set_vowel(char)
                continue

            if char in xvowels:
                self.set_xvowel(char)
                continue

            if char in geminates:
                self.inc_geminate()
                continue

            if char == lvmarker:
                self.inc_lvmarker()
                continue

            if char == WORD_BORDER:
                # When stumbling upon a word border, e.g. ぬれ|えん,
                # the current word has finished, meaning the character
                # should be flushed.
                self.flush_char()
                continue

            if char is END_CHAR:
                self.flush_char()
                continue

            # If we're still here, that means we've stumbled upon a character
            # the machine can't deal with.
            if self.unknown_strategy == UNKNOWN_DELETE:
                continue

            if self.unknown_strategy == UNKNOWN_RAISE:
                raise UnexpectedCharacterError

            if self.unknown_strategy == UNKNOWN_INCLUDE:
                self.add_unknown_char(char)

        return self.flush_stack()
