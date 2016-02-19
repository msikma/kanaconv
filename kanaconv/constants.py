# coding=utf8
#
# (C) 2015-2016, MIT License

'''
List of constants used in the library.
'''
__all__ = [
    'HIRAGANA', 'KATAKANA', 'ROMAJI', 'EMPTY_BUFFER', 'END_CHAR',
    'CV', 'VOWEL', 'XVOWEL', 'UNKNOWN_DISCARD', 'UNKNOWN_RAISE',
    'UNKNOWN_INCLUDE'
]

HIRAGANA = 10
KATAKANA = 11
ROMAJI = 12

# The machine's constants.
END_CHAR = 14
CV = 15
VOWEL = 16
XVOWEL = 17

# Strategies for dealing with unknown characters.
UNKNOWN_DISCARD = 18
UNKNOWN_RAISE = 19
UNKNOWN_INCLUDE = 20
