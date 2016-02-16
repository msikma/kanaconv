# coding=utf8
#
# (C) 2015, MIT License

'''
Finite state machine that converts hiragana and katakana strings to rōmaji
according to Modified Hepburn transliteration rules.

Only kana and rōmaji is usable; kanji can't be used as input.

Aside from the usual kana, the following are supported:

   * The wi/we kana characters（ゐゑ・ヰヱ）
   * Rare characters that are mostly for loanwords (ヺヸヷヴゔ)
   * The repeater characters（ゝゞヽヾ）
   * The yori and koto ligatures（ゟ・ヿ）
   * Numerous punctuation and bracket characters (e.g. 【】「」・。, etc)

Conversely, the following characters and features are not supported,
with no plans to support them in the future:

   * Half width katakana (U+FF65 - U+FF9F)
   * Enclosed katakana (U+32D0 - U+32FE)
   * Katakana phonetic extensions for Ainu (U+31F0 - U+31FF)
   * Historical kana supplement (𛀀; U+1B000, 𛀁; U+1B001)
   * Enclosed signs (🈁; U+1F201, 🈂; U+1F202, 🈓; U+1F213)
   * Rare typographical symbols
   * Vertical-only symbols

The theoretical combinations yi, ye and wu don't exist, nor does the
repeater mark with handakuten.
'''
import sys
from .utils import kana_romaji_lt, merge_dicts, fw_romaji_lt
from .exceptions import (
    InvalidCharacterTypeError, UnexpectedCharacterError
)
from .charsets import (
    romaji, katakana, hiragana, lvmarker, fw_romaji, punctuation
)
from .constants import *


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

# String replacement table, including the punctuation characters.
repl = merge_dicts(
    katakana['replacements'], hiragana['replacements'], punctuation,
    # Add the lookup table for fullwidth romaji.
    fw_romaji_lt(list(fw_romaji['full']), list(fw_romaji['regular']))
)

# We use sets to be able to do quick lookups.
cvs = set(cv_lt)
vowels = set(vowel_lt)
xvowels = set(xvowel_lt)
di_a = set(di_a_lt)
di_b = set(di_b_lt)
geminates = {katakana['geminate'], hiragana['geminate']}

# Repeater characters (with and without dakuten).
rpts = {katakana['repeater'], hiragana['repeater']}
drpts = {katakana['repeater_dakuten'], hiragana['repeater_dakuten']}

# The lookup tables of characters that can have a (han)dakuten, and their sets.
dkt_lt = merge_dicts(katakana['dakutenize'], hiragana['dakutenize'])
dkt_cvs = set(dkt_lt)
hdkt_lt = merge_dicts(katakana['handakutenize'], hiragana['handakutenize'])
hdkt_cvs = set(hdkt_lt)

# The singular dakuten characters.
dkt = {hiragana['dakuten'], hiragana['spacing_dakuten']}
hdkt = {hiragana['handakuten'], hiragana['spacing_handakuten']}

# Character combinations that can become long vowels,
# notwithstanding the usage of the long vowel marker.
lv_combinations = {('a', 'a'), ('u', 'u'), ('e', 'e'), ('o', 'o'), ('o', 'u')}

# Characters that trigger an apostrophe after a lone 'n'.
n_apostrophe = {'a', 'i', 'u', 'e', 'o', 'y'}

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

# Whether we're on Python 2--used for some legacy compatibility code.
PYTHON_2 = sys.version_info < (3, 0)


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
        self.unknown_char = None

        # The character stack, containing the characters of the rōmaji output.
        self.stack = []

        # Number of long vowel markers in the state.
        self.lvmarker_count = 0

        # The ウ flag: whether a long vowel marker was added due to the
        # presence of a ウ. Needed in case of the 'w' exception.
        self.has_u_lvm = False

        # Number of geminate markers in the state.
        self.geminate_count = 0

        # The character that will directly follow the flushed character.
        self.next_char_info = None
        self.next_char_type = None

        # The currently active vowel character.
        self.active_vowel = None
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
            self.active_vowel = None
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
            self.has_u_lvm = False
            self.unknown_char = None

    def set_unknown_strategy(self, behavior):
        '''
        Sets the strategy for dealing with unknown characters.
        '''
        self.unknown_strategy = behavior

    def empty_stack(self):
        '''
        Empties the stack, making the converter ready for the next
        transliteration job. Performed once after we finish one string of
        input.
        '''
        self.stack = []

    def append_unknown_char(self):
        '''
        Appends the unknown character, in case one was encountered.
        '''
        if self.unknown_strategy == UNKNOWN_INCLUDE and \
           self.unknown_char is not None:
            self.append_to_stack(self.unknown_char)

        self.unknown_char = None

    def flush_char(self):
        '''
        Appends the rōmaji characters that represent the current state
        of the machine. For example, if the state includes the character
        ト, plus a geminate marker and a long vowel marker, this causes
        the characters "ttō" to be added to the output.
        '''
        # Ignore in case there's no active character, only at the
        # first iteration of the conversion process.
        if self.active_char is None:
            # Only exception is if we've got an unknown character.
            if self.unknown_char is not None:
                self.append_unknown_char()

            return

        char_info = self.active_char_info
        char_type = self.active_char_type
        char_ro = char_info[0]
        xv = self.active_xvowel_info
        di_b = self.active_digraph_b_info
        gem = self.geminate_count
        lvm = self.lvmarker_count

        # Check for special combinations. This is exceptional behavior
        # for very specific character combinations, too unique to
        # build into the data model for every kana.
        # If a special combination is found, we'll replace the
        # rōmaji character we were planning on flushing.
        if char_type == VOWEL and len(char_info) >= 3 and xv is not None:
            try:
                exc = char_info[2]['xv'][xv[0]]
                # Found a special combination. Replace the rōmaji character.
                char_ro = exc
            except (IndexError, KeyError):
                # IndexError: no 'xv' exceptions list for this vowel.
                # KeyError: no exception for the current small vowel.
                pass

        # Check whether we're dealing with a valid char type.
        if char_type not in CHAR_TYPES:
            raise InvalidCharacterTypeError

        # If no modifiers are active (geminate marker, small vowel marker,
        # etc.) then just the currently active character is flushed.
        # We'll also continue if the character is 'n', which has a special
        # case attached to it that we'll tackle down below.
        if xv is di_b is None and gem == lvm == 0 and char_ro != 'n':
            self.append_to_stack(char_ro)
            self.append_unknown_char()
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

        # Append unknown the character as well.
        self.append_unknown_char()
        self.set_state(EMPTY_BUFFER)

    def append_to_stack(self, string):
        '''
        Appends a string to the output stack.
        '''
        self.stack.append(string)

    def add_unknown_char(self, string):
        '''
        Adds an unknown character to the stack.
        '''
        self.unknown_char = string
        self.flush_char()

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

        In some cases, the ウ becomes a consonant-vowel if it's
        paired with a small vowel. We will not know this until we see
        what comes after the ウ, so there's some backtracking
        if that's the case.
        '''
        vowel_info = kana_lt[vowel]
        vowel_ro = self.active_vowel_ro

        if self.is_long_vowel(vowel_ro, vowel_info[0]):
            # Check to see if the current vowel is ウ. If so,
            # we might need to backtrack later on in case the 'u'
            # turns into 'w' when ウ is coupled with a small vowel.
            if vowel_ro == 'u':
                self.has_u_lvm = True

            self.inc_lvmarker()
        else:
            # Not the same, so flush the active character and continue.
            self.set_char(vowel, VOWEL)

        self.active_vowel_info = vowel_info
        self.active_vowel = vowel

    def set_xvowel(self, xvowel):
        '''
        Sets the currently active small vowel, e.g. ァ.

        If an active small vowel has already been set, the current character
        must be flushed. (Double small vowels don't occur in dictionary
        words.) After that, we'll set the current character to this small
        vowel; in essence, it will act like a regular size vowel.

        We'll check for digraphs too, just so e.g. しょ followed by ぉ acts
        like a long vowel marker. This doesn't occur in dictionary words,
        but it's the most sensible behavior for unusual input.

        If the currently active character ends with the same vowel as this
        small vowel, a long vowel marker is added instead.
        E.g. テェ becomes 'tē'.
        '''
        xvowel_info = kana_lt[xvowel]
        vowel_info = self.active_vowel_info
        digraph_b_info = None

        # Special case: if the currently active character is 'n', we must
        # flush the character and set this small vowel as the active character.
        # This is because small vowels cannot affect 'n' like regular
        # consonant-vowel pairs.
        curr_is_n = self.active_vowel_ro == 'n'

        # Special case: if we've got an active vowel with special cases
        # attached to it (only ウ), and the small vowel that follows it
        # activates that special case, we may need to backtrack a bit.
        # This is because ウ is normally 'u' but becomes 'w' if there's
        # a small vowel right behind it (except the small 'u').
        # The 'w' behaves totally different from a standard vowel.
        if self.has_u_lvm and \
           xvowel_info is not None and \
           vowel_info is not None and \
           len(vowel_info) > 2 and \
           vowel_info[2].get('xv') is not None and \
           vowel_info[2]['xv'].get(xvowel_info[0]) is not None:
            # Decrement the long vowel marker, which was added on the
            # assumption that the 'u' is a vowel.
            self.dec_lvmarker()
            # Save the current vowel. We'll flush the current character,
            # without this vowel, and then set it again from a clean slate.
            former_vowel = self.active_vowel
            self.active_vowel_info = None
            self.flush_char()
            self.set_char(former_vowel, VOWEL)

        if self.active_vowel_ro == xvowel_info[0]:
            # We have an active character whose vowel is the same.
            self.inc_lvmarker()
        elif self.has_xvowel is True:
            # We have an active small vowel already. Flush the current
            # character and act as though the current small vowel
            # is a regular vowel.
            self.flush_char()
            self.set_char(xvowel, XVOWEL)
            return
        elif self.has_digraph_b is True:
            # We have an active digraph (two parts).
            digraph_b_info = self.active_digraph_b_info

        if curr_is_n:
            self.set_char(xvowel, XVOWEL)
            return

        if digraph_b_info is not None:
            # todo: too long!
            if self.is_long_vowel(self.active_vowel_ro, digraph_b_info[0]) or \
               self.is_long_vowel(self.active_digraph_b_info[0], digraph_b_info[0]):
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

    def dec_lvmarker(self):
        '''
        Decrements the long vowel marker count, unless it would become
        a negative value.
        '''
        if self.lvmarker_count == 0:
            return

        self.lvmarker_count -= 1

    def flush_stack(self):
        '''
        Returns the final output and resets the machine's state.
        '''
        output = ''.join(self.stack)
        self.set_state(EMPTY_BUFFER)
        self.empty_stack()

        if not PYTHON_2:
            return output
        else:
            return unicode(output)

    def preprocess(self, chars):
        '''
        Performs string preprocessing before the main conversion algorithm
        is used. Simple string replacements (for example, fullwidth rōmaji
        to regular rōmaji) are performed at this point.
        '''
        chars = self.normalize_dakuten(chars)
        chars = self.process_repeaters(chars)
        chars = self.perform_replacements(chars)

        return chars

    def perform_replacements(self, chars):
        '''
        Performs simple key/value string replacements that require no logic.
        This is used to convert the fullwidth rōmaji, several ligatures,
        and the punctuation characters.
        '''
        for n in range(len(chars)):
            char = chars[n]
            if char in repl:
                chars[n] = repl[char]

        # Some replacements might result in multi-character strings
        # being inserted into the list. Ensure we still have a list
        # of single characters for iteration.
        return list(''.join(chars))

    def normalize_dakuten(self, chars):
        '''
        Replaces the dakuten and handakuten modifier character combinations
        with single characters. For example, か\u3099か becomes がけ,
        or は゜は becomes ぱは.
        '''
        prev = None
        prev_n = None

        # Set all repeater characters to 0 initially,
        # then go through the list and remove them all.
        for n in range(len(chars)):
            char = chars[n]

            if char in dkt:
                chars[n] = 0
                if prev in dkt_cvs:
                    chars[prev_n] = dkt_lt[prev]

            if char in hdkt:
                chars[n] = 0
                if prev in hdkt_cvs:
                    chars[prev_n] = hdkt_lt[prev]

            prev = char
            prev_n = n

        # Remove all 0 values. There should not be any other than the ones we
        # just added. (This could use (0).__ne__, but that's Python 3 only.)
        return list(filter(lambda x: x is not 0, chars))

    def process_repeaters(self, chars):
        '''
        Replace all repeater characters (e.g. turn サヾエ into サザエ).
        '''
        prev = None
        for n in range(len(chars)):
            char = chars[n]
            if char in rpts:
                # The character is a repeater.
                chars[n] = prev

            if char in drpts:
                # The character is a repeater with dakuten.
                # If the previous character can have a dakuten, add that
                # to the stack; if not, just add whatever we had previously.
                if prev in dkt_cvs:
                    chars[n] = dkt_lt[prev]
                else:
                    chars[n] = prev

            prev = char

        return chars

    def to_romaji(self, input):
        '''
        Converts kana input to rōmaji and returns the result.
        '''
        chars = list(input)

        # Preprocess the input, making string replacements where needed.
        chars = self.preprocess(chars)

        chars.append(END_CHAR)
        for char in chars:
            if char in di_a:
                self.set_digraph_a(char)
                continue

            if char in di_b:
                self.set_digraph_b(char)
                continue

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
                # The default strategy.
                self.add_unknown_char(char)

        return self.flush_stack()
