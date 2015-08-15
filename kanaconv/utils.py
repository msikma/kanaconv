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
# The ranges are inclusive.
offsets = {
    KATAKANA: {
        'range': [0x30A0, 0x30FF],
        'direction': 1
    },
    HIRAGANA: {
        'range': [0x3040, 0x309F],
        'direction': -1
    }
}
# The total distance between both blocks.
block_offset = offsets[KATAKANA]['range'][0] - offsets[HIRAGANA]['range'][0]


def switch_charset(characters, target=''):
    '''
    Transforms an iterable of kana characters to its opposite script.
    For example, it can turn [u'あ', u'い'] into [u'ア', u'イ'].

    There are no safety checks--keep in mind that the correct source and target
    values must be set, otherwise the resulting characters will be garbled.
    '''
    # todo: better way to copy a list?
    characters = [] + characters
    offset = block_offset * offsets[target]['direction']
    for n in range(len(characters)):
        chars = list(characters[n])

        for m in range(len(chars)):
            char = chars[m]
            chars[m] = chr(ord(char) + offset)

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
