# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
A set of functions that process the basic kana information tables so that
it's easier to perform quick lookups.
'''

# Constants to avoid typoes.
HIRAGANA = 'hiragana'
KATAKANA = 'katakana'
ROMAJI = 'romaji'


def zip_kana(romaji_charset, kana_charset, add_geminate=False):
    '''
    Zips together two lists of Japanese characters, including (optionally) the
    geminate marker variants. The list is then sorted by kana string length.

    The output is like this:

       [('kkya', 'ッキャ', 3),
        ('kkyu', 'ッキュ', 3),
        [...]
        ('e', 'ェ', 1),
        ('o', 'ォ', 1)]

    This list can then be used to quickly find-replace either kana script
    to rōmaji.
    '''
    output = []
    consonants = romaji_charset['consonants']
    geminate = kana_charset['geminate']

    romaji_all = romaji_charset['all']
    kana_all = kana_charset['all']

    for n in xrange(len(kana_all)):
        # Roll over to the start of the array in case the kana charset
        # is longer than the rōmaji charset.
        ro = romaji_all[n % len(romaji_all)]
        ro = ro[1:] if ro[0] is '_' else ro
        ka = kana_all[n]
        output.append((ro, ka, len(ka)))

        # If we're adding geminate marker variants, do a check to see if
        # we're dealing with a consonant. E.g. 'ka' needs a 'kka' variant,
        # but 'a' does not.
        if add_geminate and ro[0] in consonants:
            ro = ro[0] + ro
            ka = geminate + ka
            output.append((ro, ka, len(ka)))

    # Now sort the list on kana string length, descending order.
    return sorted(output, key=lambda x: len(x[1]), reverse=True)


def romaji_lt(romaji_charset, hiragana_charset, katakana_charset):
    '''
    Creates a lookup table mapping rōmaji characters to their hiragana and
    katakana equivalents. This is later used to be able to generate the
    vowel/consonant lookup tables.
    '''
    table = {
        HIRAGANA: {},
        KATAKANA: {}
    }
    for n in xrange(len(romaji_charset)):
        romaji_char = romaji_charset[n]
        hiragana_char = hiragana_charset[n]
        katakana_char = katakana_charset[n]
        table[HIRAGANA][romaji_char] = hiragana_char
        table[KATAKANA][romaji_char] = katakana_char

    return table


def _get_char_vc(ka, ro, geminate, vowels, romaji_kana_lt):
    '''
    Returns the kana vowel/consonant lookup table for a specific character
    including, if applicable, the character preceded by a geminate marker.

    Example output for ワ:

       {'ッワ': {'romaji': {'consonant': 'w', 'full': 'wwa', 'vowel': 'a'},
                   'vowel': 'a'},
        'ワ': {'pure_vowel': False,
                'romaji': {'consonant': 'w', 'full': 'wa', 'vowel': 'a'},
                'vowel': 'ア'}}

    Pure vowels like ア don't get the extra geminate marker entry.
    '''
    result = {}

    # First letter of the rōmaji value, to determine the type of
    # kana character we're processing.
    ro_first = ro[0]

    # Special case: for the small kana characters, e.g. ぁ, the first
    # character is indicated by an underscore. Cut out the underscore
    # to get the actual rōmaji value.
    if ro_first == '_':
        ro_first = ro[1]
        ro = ro[1:]

    ro_last = ro[-1]
    char_info = {
        'romaji': {
            'full': ro,
            'vowel': ro_last
        }
    }

    # In all cases but ん, the character will have a vowel.
    # Add it here, and save it so we can add it to the geminate
    # marker entry as well.
    is_vowel = ro_last in vowels
    if is_vowel:
        ka_vowel = romaji_kana_lt[ro_last]
        char_info['vowel'] = ka_vowel
        # Characters that do not have a consonant, e.g. ア and イ,
        # are considered "pure vowels".
        char_info['pure_vowel'] = ka_vowel == ka

    # Add the consonant character in case this character
    # contains one, e.g. r for ラ.
    has_consonant = ro_first is not ro_last or ro_first not in vowels
    if has_consonant:
        char_info['romaji']['consonant'] = ro_first

    result[ka] = char_info

    # Add the geminate entry, e.g. った for た.
    if has_consonant:
        ka_geminate = geminate + ka
        char_info = {
            'romaji': {
                'full': ro_first + ro,
                'vowel': ro_last,
                'consonant': ro_first
            }
        }
        if is_vowel:
            char_info['vowel'] = 'a'

        result[ka_geminate] = char_info

    return result


def _get_charset_vc(romaji_charset, kana_charset):
    '''
    Returns the kana vowel/consonant lookup table for one specific character
    set.
    '''
    romaji_all = romaji_charset['all']
    vowels = romaji_charset['vowels']

    geminate = kana_charset['geminate']
    kana_all = kana_charset['all']

    # The lookup table between rōmaji and this kana character set.
    romaji_kana_lt = romaji_charset['kana_lt'][kana_charset['type']]

    result = {}

    for n in xrange(len(kana_all)):
        ka = kana_all[n]
        ro = romaji_all[n % len(romaji_all)]
        chars = _get_char_vc(ka, ro, geminate, vowels, romaji_kana_lt)
        result.update(chars)

    return result


def generate_vc_lt(romaji_charset, *kana_charsets):
    '''
    Generates a vowel/consonant lookup table that uses kana characters as the
    keys, with each value including the following:

       * Rōmaji equivalent
       * Rōmaji vowel
       * Rōmaji consonant
       * Kana vowel (e.g. ア for ラ)

    Entries that include an extra leading geminate marker are also generated.
    '''
    table = {}

    for kana_charset in kana_charsets:
        kana = _get_charset_vc(romaji_charset, kana_charset)
        table.update(kana)

    return table
