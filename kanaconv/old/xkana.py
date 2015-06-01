# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
Converts strings from katakana to hiragana and vice versa.

The conversion process is mostly very straightforward, but edge cases are
accounted for. The script can optionally convert contiguous vowels into
the long vowel marker character (e.g. らあめん becomes ラーメン) and the
other way around.
'''
from kanaconv.constants import hiragana_charset, katakana_charset, \
    kana_vc_lt, lvm
from kanaconv.exceptions import InvalidScriptError


charsets = {
    'katakana': {
        # Some strings are unique to this charset and should not be converted.
        'unique': katakana_charset['unique'],
        'range': katakana_charset['range'],
        'direction': 1
    },
    'hiragana': {
        'unique': hiragana_charset['unique'],
        'range': hiragana_charset['range'],
        'direction': -1
    }
}

# The offset from the katakana Unicode block to the hiragana block.
block_offset = charsets['katakana']['range'][0] -\
    charsets['hiragana']['range'][0]

# Constants for specifying which transformation we want.
HIRAGANA = 'hiragana'
KATAKANA = 'katakana'
VALID = [HIRAGANA, KATAKANA]


def kana_to_kana(string, source='', target='', convert_lvm=True):
    '''
    Converts a string from one kana script to another.
    '''
    if source not in VALID or target not in VALID:
        raise InvalidScriptError

    source_cs = charsets[source]
    target_cs = charsets[target]

    # Select the range of the source character set.
    range = source_cs['range']
    offset = block_offset * target_cs['direction']
    unique = source_cs['unique']

    if convert_lvm:
        string = normalize_lvm(string, target)

    # Array containing the characters of the translated string.
    trns = []

    for n in xrange(len(string)):
        char = string[n]
        char_ord = ord(char)

        # Check if this character is within range. Characters that do not match
        # or appear in the list of unique characters are unaffected.
        if range[0] <= char_ord <= range[1] and char not in unique:
            trns.append(unichr(char_ord + offset))
        else:
            trns.append(char)

    return ''.join(trns)


def normalize_dakuten(string):
    # todo: add code here to normalize the dakuten, i.e. replace it with
    # proper precompiled ones
    return string


def replace_punctuation(string):
    # todo: add code here to replace all punctuation characters
    return string


def kata_to_hira(string):
    '''
    Converts a katakana string to hiragana.
    '''
    return kana_to_kana(string, source=KATAKANA, target=HIRAGANA)


def hira_to_kata(string):
    '''
    Converts a hiragana string to katakana.
    '''
    return kana_to_kana(string, source=HIRAGANA, target=KATAKANA)


def normalize_lvm(string, target=''):
    '''
    Replaces parts of a string to conform to either hiragana or katakana
    conventions regarding contiguous vowels. This is an optional processing
    step when converting from one kana script to another.
    '''
    if target not in VALID:
        raise InvalidScriptError

    # When targeting hiragana, the lvm should be replaced with the
    # preceding vowel. E.g. アゲーン becomes あげえん.

    if target is HIRAGANA:
        return _remove_lvm(string)

    if target is KATAKANA:
        return _add_lvm(string)


def _remove_lvm(string):
    '''
    Removes long vowel markers from a string and replaces them
    with repeating vowels. Used when targeting hiragana.
    '''
    source_str = string.split(lvm)
    target_str = []

    # Return early if there's no long vowel marker in the sentence.
    if len(source_str) == 1:
        return string

    # This string has at least one long vowel marker. We've split
    # the string, and now we'll run through every segment and insert
    # an appropriate hiragana character on each iteration except the last.
    # E.g., we'll change ラーメン to [ラ, メン] and then to [ラ, ア, メン].

    vowel = None
    segments = len(source_str)

    for n in xrange(segments):
        char = source_str[n]

        if n == segments - 1:
            # On the last iteration, insert only the original character,
            # since there is no vowel marker after the last item.
            target_str.append(char)
            break

        if char != '':
            # For every regular character, insert the character
            # and its corresponding vowel character.
            vowel = kana_vc_lt[char[0]]['vowel']
            target_str.append(char)
            target_str.append(vowel)
        else:
            # An empty character means there's multiple consecutive
            # vowel markers. Simply insert the vowel again.
            target_str.append(vowel)

    return ''.join(target_str)


def _add_lvm(string):
    '''
    Adds long vowel markers to a string containing repeating vowels.
    Used when targeting katakana.
    '''
    target_str = []

    # When targeting katakana, we'll replace vowel repetitions with
    # the long vowel marker. For example, てめえ is changed to テメー
    # as め and え share the same vowel.

    active_vowel = ''

    for char in string:
        # Look up character information. If the string contains
        # an unknown character, an empty dict will ensure that no
        # substitution is made.
        char_info = kana_vc_lt.get(char, {})

        vowel = char_info.get('vowel')
        is_pure_vowel = char_info.get('pure_vowel', False)
        same_as_active = vowel is active_vowel

        # Only pure vowels can be replaced by the long vowel marker.
        if not is_pure_vowel or not same_as_active:
            target_str.append(char)
            active_vowel = vowel
        else:
            target_str.append(lvm)

    return ''.join(target_str)
