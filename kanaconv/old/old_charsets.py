# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
The kana constants are defined here. This includes all hiragana and katakana
characters (as defined in several sets based on their processing needs),
as well as punctuation and other special characters, and their rōmaji
equivalents.

Additionally, read the comments in this file for information on what these
characters mean and how they're meant to be used.

Unicode ranges in this file are inclusive ranges.
'''
from kanaconv.constants import *
from kanaconv.utils import switch_charset

# For ease of processing, we've divided the kana characters into six sets.
#
# Each of these sets has its own processing needs. Both of these sets
# has a katakana and a hiragana version.

# Katakana（片仮名・カタカナ）
# Range: U+30A1 - U+30FA
katakana = {
    'type': KATAKANA,
    # Set A: capable of having a long vowel marker
    'set_a': [
        u'ア', u'イ', u'ウ', u'エ', u'オ',
        u'カ', u'キ', u'ク', u'ケ', u'コ',
        u'サ', u'シ', u'ス', u'セ', u'ソ',
        u'タ', u'チ', u'ツ', u'テ', u'ト',
        u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ',
        u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ',
        u'マ', u'ミ', u'ム', u'メ', u'モ',
        u'ヤ', u'ユ', u'ヨ',
        u'ラ', u'リ', u'ル', u'レ', u'ロ',
        u'ワ', u'ヲ',
        u'ヰ', u'ヱ',
        u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ',
        u'ヵ', u'ヶ'
    ],
    # Set B: capable of having a geminate marker
    # Note: the n-line does not actually get a geminate marker,
    # but we'll treat it as a special case in post-processing.
    'set_b': [
        u'カ', u'キ', u'ク', u'ケ', u'コ',
        u'サ', u'シ', u'ス', u'セ', u'ソ',
        u'タ', u'チ', u'ツ', u'テ', u'ト',
        u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ',
        u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ',
        u'マ', u'ミ', u'ム', u'メ', u'モ',
        u'ヤ', u'ユ', u'ヨ',
        u'ラ', u'リ', u'ル', u'レ', u'ロ',
        u'ワ', u'ヲ',
        u'ヰ', u'ヱ',
        u'ヵ', u'ヶ',
    ],
    # Set C: the first characters of the digraphs
    'set_c': [
        u'キ', u'シ', u'チ', u'ナ', u'ヒ', u'ミ', u'リ'
    ],
    # Set D: the second characters of the digraphs
    'set_d': [
        u'ャ', u'ュ', u'ョ'
    ],
    # Set E: the small vowels
    'set_e': [
        u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ'
    ],
    # Set F: the ん or ン character, which is a special case
    'set_f': [
        u'ン'
    ],
    # Geminate consonant marker（sukuon, 促音・そくおん）
    'geminate': u'ッ',
    # Rare special case: ッン is considered ン. Currently unused.
    'xtsun': {
        u'ッン': u'ン'
    },
    # The following characters are unique to the katakana Unicode block.
    'unique': [u'゠', u'ヷ', u'ヸ', u'ヹ', u'ヺ', u'・', u'ー'],
    # Repeater characters（kurikaeshi, くりかえし）
    # Used only in historical texts; these repeat the preceding character,
    # with the latter adding a dakuten
    'repeater': u'ヽ',            # サヽキ = ササキ
    'repeater_dakuten': u'ヾ',    # サヾエ = サザエ
    # Special ligature for koto (コト), generally used in vertical writing
    'koto': u'ヿ',
    # Double hyphen – used to separate multiple foreign names,
    # e.g. Russell–Einstein Manifesto (ラッセル゠アインシュタイン宣言)
    'dbl_hyph': u'゠'
}

# Hiragana（平仮名・ひらがな）
# Range: U+3041 - U+3092
hiragana = {
    'type': HIRAGANA,
    # The hiragana sets, which are the converted versions of the katakana sets.
    'set_a': switch_charset(katakana['set_a'], HIRAGANA),
    'set_b': switch_charset(katakana['set_b'], HIRAGANA),
    'set_c': switch_charset(katakana['set_c'], HIRAGANA),
    'set_d': switch_charset(katakana['set_d'], HIRAGANA),
    'set_e': switch_charset(katakana['set_e'], HIRAGANA),
    'set_f': switch_charset(katakana['set_f'], HIRAGANA),
    # Geminate consonant marker（sukuon, 促音・そくおん）
    'geminate': u'っ',
    # The following characters are unique to the hiragana Unicode block.
    'unique': [u'\u3099', u'\u309a', u'゛', u'゜'],
    # (Han)dakuten markers – note that the spacing (han)dakuten occupy a full
    # width character space and do not combine with other kana characters.
    'dakuten': u'゙',             # combining: がか (U+304B U+3099 U+304B)
    'handakuten': u'゚',          # combining: ぱは (U+306F U+309A U+306F)
    'spacing_dakuten': u'゛',     # non-combining: か゛か (U+304B U+309B U+304B)
    'spacing_handakuten': u'゜',  # non-combining: は゜は (U+306B U+309C U+306F)
    # Special ligature for yori (より)
    'yori': u'ゟ',
    # Repeater characters（kurikaeshi, くりかえし）
    # Used only in historical texts; these repeat the preceding character,
    # with the latter adding a dakuten
    'repeater': u'ゝ',            # さゝき = ささき
    'repeater_dakuten': u'ゞ'     # あひゞき = あひびき
}

# Rōmaji（ローマ字・ローマじ）
romaji_charset = {
    'type': ROMAJI,
    # Set A: capable of having a long vowel marker
    # The second character indicates the long vowel marker replacement.
    'set_a': [
        ('a', 'a'), ('i', 'i'), ('u', 'u'), ('e', 'e'), ('o', 'o'),
        ('ka', 'a'), ('ki', 'i'), ('ku', 'u'), ('ke', 'e'), ('ko', 'o'),
        ('sa', 'a'), ('shi', 'i'), ('su', 'u'), ('se', 'e'), ('so', 'o'),
        ('ta', 'a'), ('chi', 'i'), ('tsu', 'u'), ('te', 'e'), ('to', 'o'),
        ('na', 'a'), ('ni', 'i'), ('nu', 'u'), ('ne', 'e'), ('no', 'o'),
        ('ha', 'a'), ('hi', 'i'), ('fu', 'u'), ('he', 'e'), ('ho', 'o'),
        ('ma', 'a'), ('mi', 'i'), ('mu', 'u'), ('me', 'e'), ('mo', 'o'),
        ('ya', 'a'), ('yu', 'u'), ('yo', 'o'),
        ('ra', 'a'), ('ri', 'i'), ('ru', 'u'), ('re', 'e'), ('ro', 'o'),
        ('wa', 'a'), ('wo', 'o'),
        ('wi', 'i'), ('we', 'e'),
        ('a', 'a'), ('i', 'i'), ('u', 'u'), ('e', 'e'), ('o', 'o'),
        ('ka', 'a'), ('ka', 'a')
    ],
    # Set B: capable of having a geminate marker
    # The second character indicates the geminate marker replacement.
    'set_b': [
        ('ka', 'k'), ('ki', 'k'), ('ku', 'k'), ('ke', 'k'), ('ko', 'k'),
        ('sa', 's'), ('shi', 's'), ('su', 's'), ('se', 's'), ('so', 's'),
        ('ta', 't'), ('chi', 't'), ('tsu', 't'), ('te', 't'), ('to', 't'),
        ('na', 'n'), ('ni', 'n'), ('nu', 'n'), ('ne', 'n'), ('no', 'n'),
        ('ha', 'h'), ('hi', 'h'), ('fu', 'f'), ('he', 'h'), ('ho', 'h'),
        ('ma', 'm'), ('mi', 'm'), ('mu', 'm'), ('me', 'm'), ('mo', 'm'),
        ('ya', 'y'), ('yu', 'y'), ('yo', 'y'),
        ('ra', 'r'), ('ri', 'r'), ('ru', 'r'), ('re', 'r'), ('ro', 'r'),
        ('wa', 'w'), ('wo', 'w'),
        ('wi', 'w'), ('we', 'w'),
        ('ka', 'k'), ('ka', 'k')
    ],
    # Set C: the first characters of the digraphs
    # Only the first rōmaji character of the digraph is used.
    # The second character indicates the geminate marker replacement.
    'set_c': [
        ('k', 'k'), ('sh', 's'), ('ch', 't'), ('n', 'n'),
        ('h', 'h'), ('m', 'm'), ('r', 'r')
    ],
    # Set D: the second characters of the digraphs
    # The second character indicates the long vowel marker replacement.
    'set_d': [
        ('ya', 'a'), ('yu', 'u'), ('yo', 'o')
    ],
    # Set E: the small vowels
    # The second character indicates the long vowel marker replacement.
    'set_e': [
        ('a', 'a'), ('i', 'i'), ('u', 'u'), ('e', 'e'), ('o', 'o'),
    ],
    # Set F: the ん or ン character, which is a special case
    # The second character indicates the geminate marker replacement.
    'set_f': [
        ('n', 'n')
    ],
    # The macron characters used in Modified Hepburn romanization.
    'macrons': {
        'a': u'ā',
        'i': u'ī',
        'u': u'ū',
        'e': u'ē',
        'o': u'ō'
    },
    # The uppercase macron characters. Currently unused.
    'macrons_uppercase': {
        'A': u'Ā',
        'I': u'Ī',
        'U': u'Ū',
        'E': u'Ē',
        'O': u'Ō'
    }
}

# Punctuation (yakumono, 約物・やくもの)
# Unlike the preceding constants, these can be directly replaced.
punctuation = {
    # Curly brackets（namikakko, 波括弧・なみかっこ; "wave brackets"）
    u'｛': u'{',
    u'｝': u'}',
    # Parentheses（marukakko, 丸括弧・まるかっこ; "round brackets"）
    u'（': u')',
    u'）': u')',
    # Tortoise shell brackets（kikkō, 亀甲・きっこう）
    u'〔': u'[',
    u'〕': u']',
    # Square brackets（kakukakko, 角括弧・かくかっこ; "cornered brackets"）
    u'［': u'[',
    u'］': u']',
    # Lenticular（sumitsukikakko, 隅付き括弧・すみつきかっこ; "inked brackets"）
    u'【': u'[',
    u'】': u']',
    # Hill brackets（yamakakko, 山括弧・やまかっこ）
    u'〈': u'<',
    u'〉': u'>',
    # Double hill brackets (nijūyamakakko, 二重山括弧・にじゅうやまかっこ)
    u'《': u'«',
    u'》': u'»',
    # Single quotation marks（kagikakko, 鉤括弧・かぎかっこ）
    u'「': u'[',
    u'」': u']',
    # Double quotation marks（nijūkagikakko, 二重鉤括弧・にじゅうかぎかっこ）
    u'『': u'[',
    u'』': u']',
    # Ideographic comma
    u'、': u',',
    # Fullwidth comma
    u'，': u',',
    # Fullwidth space
    u'　': u' ',
    # Fullwidth tilde（nami dasshu, 波ダッシュ・なみダッシュ; "wave dash"）
    u'〜': u'~',
    # Fullwidth colon（コロン）
    u'：': u':',
    # Fullwidth exclamation mark（kantanfu, 感嘆符・かんたんふ）
    u'！': u'!',
    # Fullwidth question mark (hatena mark, はてなマーク)
    u'？': u'?',
    # Ideographic fullstop
    u'。': u'. ',
    # Two-dot ellipsis
    u'‥': u'..',
    # Middle dot – used to break up words, especially foreign names
    u'・': u' '
}

# Long vowel marker (chōuon, 長音・ちょうおん)
lvm = u'ー'
