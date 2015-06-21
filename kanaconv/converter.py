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
from kanaconv.utils import kana_romaji_lt, merge_dicts
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

# Global lookup table for all kana character types except the digraphs.
kana_lt = merge_dicts(cv_lt, vowel_lt, xvowel_lt)

# Lookup table for digraph kana.
di_a_romaji = romaji['set_digraphs_a']
di_b_romaji = romaji['set_digraphs_b']
di_a_katakana = katakana['set_digraphs_a']
di_b_katakana = katakana['set_digraphs_b']
di_a_hiragana = hiragana['set_digraphs_a']
di_b_hiragana = hiragana['set_digraphs_b']
di_a_lt = kana_romaji_lt(di_a_romaji, di_a_katakana, di_a_hiragana)
di_b_lt = kana_romaji_lt(di_b_romaji, di_b_katakana, di_b_hiragana)

# We use sets to be able to do quick lookups.
cvs = set(cv_lt)
vowels = set(vowel_lt)
xvowels = set(xvowel_lt)
di_a = set(di_a_lt)
di_b = set(di_b_lt)
geminates = {katakana['geminate'], hiragana['geminate']}

# Character combinations that can become long vowels.
lv_combinations = {('a', 'a'), ('u', 'u'), ('e', 'e'), ('o', 'o'), ('o', 'u')}

# Characters that trigger an apostrophe after a lone 'n'.
n_apostrophe = {'a', 'i', 'u', 'e', 'o', 'y'}

# The machine's constants.
EMPTY_BUFFER = 10
END_CHAR = 11
CV = 12
VOWEL = 13
XVOWEL = 14

# Strategies for dealing with unknown characters.
UNKNOWN_DELETE = 15
UNKNOWN_RAISE = 16
UNKNOWN_INCLUDE = 17

# The replacement character for impossible geminate marker combinations.
# E.g. っえ becomes -e. todo: implement
REPL_CHAR = romaji['repl_char']
# The character that follows the 'n' before vowels and 'y'.
APOSTROPHE_CHAR = romaji['apostrophe_char']

# The valid character types.
CHAR_TYPES = {CV, VOWEL, XVOWEL}

# Two special characters that change the machine's behavior.
WORD_BORDER = '|'         # word boundary, e.g. 子馬 = こ|うま = kouma, not kōma.
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
        self.unknown_strategy = UNKNOWN_INCLUDE
        self.unknown_chars = []

        # The character stack, containing the characters of the rōmaji output.
        self.stack = []

        # Number of long vowel markers in the state.
        self.lvmarker_count = 0

        # Number of geminate markers in the state.
        self.geminate_count = 0

        # The character that will directly follow the flushed character.
        self.next_char_info = None
        self.next_char_type = None

        # The currently active rōmaji vowel character.
        self.active_vowel_info = None
        self.active_vowel_ro = None

        # The currently active small vowel character.
        self.active_xvowel_info = None

        # The currently active character.
        self.active_char = None
        self.active_char_info = None

        # The type of character; either a consonant-vowel pair or a vowel.
        self.active_char_type = None

        # Information on digraph character parts.
        self.active_digraph_a_info = None
        self.active_digraph_b_info = None

        # Whether the state has a small vowel or digraph second part.
        self.has_xvowel = False
        self.has_digraph_b = False

        # Reset the machine to a pristine state.
        self.empty_stack()
        self.set_state(EMPTY_BUFFER)

    def set_state(self, state):
        '''
        Resets the machine to a specific base state.
        '''
        if state == EMPTY_BUFFER:
            self.lvmarker_count = 0
            self.geminate_count = 0
            self.next_char_info = None
            self.next_char_type = None
            self.active_vowel_info = None
            self.active_vowel_ro = None
            self.active_xvowel_info = None
            self.active_char = None
            self.active_char_info = None
            self.active_char_type = None
            self.active_digraph_a_info = None
            self.active_digraph_b_info = None
            self.has_xvowel = False
            self.has_digraph_b = False
            self.unknown_chars = []

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
        print('-------- flush char %s' % (repr(self.active_char_info)))
        if self.active_char is None:
            # Ignore in case there's no active character, only at the very
            # beginning of the conversion process.
            return

        char_info = self.active_char_info
        char_type = self.active_char_type
        char_ro = char_info[0]
        xv = self.active_xvowel_info
        di_b = self.active_digraph_b_info
        gem = self.geminate_count
        lvm = self.lvmarker_count

        # Check whether we're dealing with a valid char type.
        if char_type not in CHAR_TYPES:
            raise InvalidCharacterTypeError

        # If no modifiers are active (geminate marker, small vowel marker,
        # etc.) then just the currently active character is flushed.
        # We'll also continue if the character is 'n', which has a special
        # case attached to it that we'll tackle down below.
        if xv is di_b is None and gem == lvm == 0 and char_ro != 'n':
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

            # If this flushed character is an 'n', and precedes a vowel or
            # a 'y' consonant, it must be followed by an apostrophe.
            char_apostrophe = ''
            if char_ro == 'n' and self.next_char_info is not None:
                first_char = None

                if self.next_char_type == CV:
                    first_char = self.char_ro_consonant(self.next_char_info, CV)

                if self.next_char_type == VOWEL or \
                   self.next_char_type == XVOWEL:
                    first_char = self.char_ro_vowel(self.next_char_info, VOWEL)

                # If the following character is in the set of characters
                # that should trigger an apostrophe, add it to the output.
                if first_char in n_apostrophe:
                    char_apostrophe = APOSTROPHE_CHAR

            # Check to see if we've got a full digraph.
            if self.active_digraph_a_info is not None and \
               self.active_digraph_b_info is not None:
                char_cons = self.active_digraph_a_info[0]

            # Determine the geminate consonant part (which can be
            # arbitrarily long).
            gem_cons = char_gem_cons * gem

            if xv is not None:
                # Combine the consonant of the character with the small vowel.
                # Use a macron vowel if there's a long vowel marker,
                # else use the regular vowel.
                vowel = xv[1] * lvm if lvm > 0 else xv[0]
            elif di_b is not None:
                # Put together the digraph. Here we produce the latter half
                # of the digraph.
                vowel = di_b[1] * lvm if lvm > 0 else di_b[0]
            else:
                # Neither a small vowel marker, nor a digraph.
                vowel = ''

            if vowel != '':
                # If we've got a special vowel part, combine it with the
                # main consonant.
                char_main = char_cons + char_apostrophe + vowel
            else:
                # If not, process the main character and add the long vowels
                # if applicable.
                if lvm > 0:
                    char_main = char_cons + char_apostrophe + char_lv * lvm
                else:
                    char_main = char_ro + char_apostrophe

            self.append_to_stack(gem_cons + char_main)

        if char_type == VOWEL or char_type == XVOWEL:
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
        '''
        Returns all unknown characters in the stack as a string.
        '''
        return ''.join(self.unknown_chars)

    def add_unknown_char(self, string):
        '''
        Adds an unknown character to the stack.
        '''
        self.unknown_chars.append(string)

    def set_digraph_a(self, char):
        '''
        Sets the currently active character, in case it is (potentially)
        the first part of a digraph.
        '''
        self.set_char(char, CV)
        self.active_digraph_a_info = di_a_lt[char]

    def set_digraph_b(self, char):
        '''
        Sets the second part of a digraph.
        '''
        self.has_digraph_b = True
        # Change the active vowel to the one provided by the second part
        # of the digraph.
        self.active_vowel_ro = di_b_lt[char][0]
        self.active_digraph_b_info = di_b_lt[char]

    def char_lookup(self, char):
        '''
        Retrieves a character's info from the lookup table.
        '''
        return kana_lt[char]

    def char_ro_consonant(self, char_info, type):
        '''
        Returns the consonant part of a character in rōmaji.
        '''
        if type == CV:
            return char_info[1]

        return None

    def char_ro_vowel(self, char_info, type):
        '''
        Returns the vowel part of a character in rōmaji.
        '''
        if type == CV:
            return char_info[3]

        if type == VOWEL or type == XVOWEL:
            return char_info[0]

        return None

    def set_char(self, char, type):
        '''
        Sets the currently active character, e.g. ト. We save some information
        about the character as well. active_char_info contains the full
        tuple of rōmaji info, and active_ro_vowel contains e.g. 'o' for ト.

        We also set the character type: either a consonant-vowel pair
        or a vowel. This affects the way the character is flushed later.
        '''
        self.next_char_info = self.char_lookup(char)
        self.next_char_type = type
        self.flush_char()

        self.active_char = char
        self.active_char_type = type

        print('  char: %s' % char)

        self.active_char_info = self.char_lookup(char)
        self.active_vowel_ro = self.char_ro_vowel(self.active_char_info, type)

    def is_long_vowel(self, vowel_ro_a, vowel_ro_b):
        '''
        Checks whether two rōmaji vowels combine to become a long vowel.
        True for a + a, u + u, e + e, o + o, and o + u. The order of
        arguments matters for the o + u combination.
        '''
        return (vowel_ro_a, vowel_ro_b) in lv_combinations

    def set_vowel(self, vowel):
        '''
        Sets the currently active vowel, e.g. ア.

        Vowels act slightly differently from other characters. If one
        succeeds the same vowel (or consonant-vowel pair with the same vowel)
        then it acts like a long vowel marker. E.g. おねえ becomes onē.

        Hence, either we increment the long vowel marker count, or we
        flush the current character and set the active character to this.
        '''
        if self.is_long_vowel(self.active_vowel_ro, kana_lt[vowel][0]):
            # Same vowel as the one that's currently active.
            self.inc_lvmarker()
        else:
            # Not the same, so flush the active character and continue.
            self.set_char(vowel, VOWEL)

    def set_xvowel(self, xvowel):
        '''
        Sets the currently active small vowel, e.g. ァ.

        If an active small vowel has already been set (which doesn't occur in
        dictionary words), the current character must be flushed. After that,
        we'll set the current character to this small vowel; in essence,
        it will act like a regular size vowel.

        We'll check for digraphs too, just so e.g. しょ followed by ぉ acts
        like a long vowel marker. This doesn't occur in dictionary words,
        but it's the most sensible behavior for unusual input.

        If the currently active character ends with the same vowel as this
        small vowel, a long vowel marker is added instead.
        E.g. テェ becomes 'tē'.
        '''
        xvowel_info = kana_lt[xvowel]
        vowel_info = None

        # Special case: if the currently active character is 'n', we must
        # flush the character and set this small vowel as the active character.
        # This is because small vowels cannot affect 'n' like regular
        # consonant-vowel pairs.
        curr_is_n = self.active_vowel_ro == 'n'

        if self.active_vowel_ro == xvowel_info[0]:
            # We have an active character whose vowel is the same.
            self.inc_lvmarker()
        elif self.has_xvowel is True or curr_is_n:
            # We have an active small vowel already.
            vowel_info = self.active_xvowel_info
        elif self.has_digraph_b is True:
            # We have an active digraph (two parts).
            vowel_info = self.active_digraph_b_info

        if curr_is_n:
            self.set_char(xvowel, XVOWEL)
            return

        if vowel_info is not None:
            if self.is_long_vowel(self.active_vowel_ro, vowel_info[0]) or \
               self.is_long_vowel(self.active_digraph_b_info[0], vowel_info[0]):
                # Same vowel as the one that's currently active.
                self.inc_lvmarker()
            else:
                # Not the same, so flush the active character and continue.
                self.active_vowel_ro = self.active_xvowel_info[0]
                self.set_char(xvowel, XVOWEL)
        else:
            self.active_xvowel_info = xvowel_info

        self.has_xvowel = True

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
        # Ignore the long vowel marker in case it occurs before any
        # characters that it can affect.
        if self.active_char is None:
            return

        self.lvmarker_count += 1

    def flush_stack(self):
        '''
        Returns the final output and resets the machine's state.
        '''
        output = ''.join(self.stack)
        self.set_state(EMPTY_BUFFER)
        self.empty_stack()
        return unicode(output)

    def to_romaji(self, input):
        '''
        Converts kana input to rōmaji and returns the result.
        '''
        chars = list(input)
        chars.append(END_CHAR)
        for char in chars:
            if char in di_a:
                print('set_digraph_a(%s)' % (char))
                self.set_digraph_a(char)
                continue

            if char in di_b:
                print('set_digraph_b(%s)' % (char))
                self.set_digraph_b(char)

            if char in cvs:
                print('set_char(%s, %s)' % (char, CV))
                self.set_char(char, CV)
                continue

            if char in vowels:
                print('set_vowel(%s)' % (char))
                self.set_vowel(char)
                continue

            if char in xvowels:
                print('set_xvowel(%s)' % (char))
                self.set_xvowel(char)
                continue

            if char in geminates:
                print('inc_geminate()')
                self.inc_geminate()
                continue

            if char == lvmarker:
                print('inc_lvmarker()')
                self.inc_lvmarker()
                continue

            if char == WORD_BORDER:
                # When stumbling upon a word border, e.g. in ぬれ|えん,
                # the current word has finished, meaning the character
                # should be flushed.
                self.flush_char()
                continue

            if char == END_CHAR:
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
