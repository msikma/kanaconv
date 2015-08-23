# coding=utf8
#
# (C) 2015, MIT License

'''
Helper utilities to make processing easier.
'''
import sys
from kanaconv.constants import KATAKANA, HIRAGANA

# Set the correct code point function based on whether we're on Python 2 or 3.
if sys.version_info < (3, 0):
    chr = unichr

# The start and end offsets of the hiragana and katakana Unicode blocks.
# The ranges are inclusive and include only printable kana characters,
# e.g. あ, ぃ, ヸ, etc.
offsets = {
    KATAKANA: {
        'start': 0x30A0,
        'range': [0x30A1, 0x30FA],
        'direction': 1
    },
    HIRAGANA: {
        'start': 0x3040,
        'range': [0x3041, 0x3096],
        'direction': -1
    }
}
# The total distance between both blocks.
block_offset = offsets[KATAKANA]['start'] - offsets[HIRAGANA]['start']


def in_range(offset, target=''):
    '''
    Returns whether a particular offset is within the range of printable
    kana characters.
    '''
    range = offsets[target]['range']
    return range[0] <= offset <= range[1]


def switch_charset(characters, target=''):
    '''
    Transforms an iterable of kana characters to its opposite script.
    For example, it can turn [u'あ', u'い'] into [u'ア', u'イ'],
    or {u'ホ': u'ボ} into {u'ほ': u'ぼ'}.

    There are no safety checks--keep in mind that the correct source and target
    values must be set, otherwise the resulting characters will be garbled.
    '''
    if isinstance(characters, dict):
        return _switch_charset_dict(characters, target)
    else:
        return _switch_charset_list(characters, target)


def _switch_charset_dict(characters, target=''):
    '''
    Switches the character set of the key/value pairs in a dictionary.
    '''
    offset_characters = {}
    offset = block_offset * offsets[target]['direction']
    for char in characters:
        offset_key = chr(ord(char) + offset)
        offset_value = chr(ord(characters[char]) + offset)
        offset_characters[offset_key] = offset_value

    return offset_characters

def _switch_charset_list(characters, target=''):
    '''
    Switches the character set of a list. If a character does not have
    an equivalent in the target script (e.g. ヹ when converting to hiragana),
    the original character is kept.
    '''
    # Copy the list to avoid modifying the existing one.
    characters = characters[:]
    offset = block_offset * offsets[target]['direction']
    for n in range(len(characters)):
        chars = list(characters[n])

        for m in range(len(chars)):
            char = chars[m]
            char_offset = ord(char) + offset
            # Verify that the offset character is within the valid range.
            if in_range(char_offset, target):
                chars[m] = chr(char_offset)
            else:
                chars[m] = char

        characters[n] = ''.join(chars)

    return characters


def merge_dicts(*dicts):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.

    Taken from an answer by Aaron Hall on Stack Overflow:
    <http://stackoverflow.com/a/26853961>.
    '''
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


def kana_romaji_lt(romaji, *kana):
    '''
    Generates a lookup table with the kana characters on the left side
    and their rōmaji equivalents as the values.

    For the consonant-vowel (cv) characters, we'll generate:

       {u'か': ('ka', 'k', 'k', 'ā'),
        u'が': ('ga', 'g', 'g', 'ā'),
        [...]

    Multiple kana character sets can be passed as rest arguments.
    '''
    lt = {}
    for kana_set in kana:
        for n in range(len(romaji)):
            ro = romaji[n]
            ka = kana_set[n]
            lt[ka] = ro

    return lt


def fw_romaji_lt(full, regular):
    '''
    Generates a lookup table with the fullwidth rōmaji characters
    on the left side, and the regular rōmaji characters as the values.
    '''
    lt = {}
    for n in range(len(full)):
        fw = full[n]
        reg = regular[n]
        lt[fw] = reg

    return lt
