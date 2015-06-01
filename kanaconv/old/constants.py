# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
The kana constants are defined here. This includes all hiragana and katakana
characters and their (han)dakuten variants, as well as all other characters
that are relevant for the conversion of words and texts.

Additionally, read the comments in this file for information on what these
characters mean and how they're meant to be used.

Unicode ranges in this file are inclusive ranges.
'''
from kanaconv.utils import romaji_lt, generate_vc_lt, zip_kana


# Constants to avoid typoes.
HIRAGANA = 'hiragana'
KATAKANA = 'katakana'
ROMAJI = 'romaji'

# Rōmaji（ローマ字・ローマじ）
romaji_charset = {
    'type': ROMAJI,
    # Monograph equivalents
    'mono': [
        'a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko',
        'sa', 'shi', 'su', 'se', 'so', 'ta', 'chi', 'tsu', 'te', 'to',
        'na', 'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'fu', 'he', 'ho',
        'ma', 'mi', 'mu', 'me', 'mo', 'ya', 'yu', 'yo', 'ra', 'ri',
        'ru', 're', 'ro', 'wa', 'wo', 'n',
        # Obsolete characters
        'wi', 'wu',
        # Small characters; note that ヵ and ヶ are both transliterated to ka.
        # These have an underscore prefix to prevent them from clashing with
        # the main characters.
        '_a', '_i', '_u', '_e', '_o', '_ka', '_ka'
    ],
    # Digraph equivalents
    'di': [
        'kya', 'kyu', 'kyo', 'sha', 'shu', 'sho', 'cha', 'chu', 'cho',
        'nya', 'nyu', 'nyo', 'hya', 'hyu', 'hyo', 'mya', 'myu', 'myo',
        'rya', 'ryu', 'ryo'
    ],
    # A list of consonants, to check whether the geminate marker applies.
    'consonants': [
        'c', 'f', 'h', 'k', 'm', 'n', 'r', 's', 't', 'w', 'y'
    ],
    # A list of vowels, to check whether the long vowel marker applies.
    'vowels': [
        'a', 'i', 'u', 'e', 'o'
    ],
    # The macron characters used in Modified Hepburn romanization.
    'macrons': {
        'aa': u'ā',
        'ii': u'ī',
        'uu': u'ū',
        'ee': u'ē',
        'oo': u'ō'
    },
    # The uppercase macron characters. Currently unused.
    'macrons_uppercase': {
        'AA': u'Ā',
        'II': u'Ī',
        'UU': u'Ū',
        'EE': u'Ē',
        'OO': u'Ō'
    }
}

# Hiragana（平仮名・ひらがな）
# Range: U+3041 - U+3092
hiragana_charset = {
    'type': HIRAGANA,
    # Monographs（gojūon, 五十音・ごじゅうおん）
    'mono': [
        u'あ', u'い', u'う', u'え', u'お', u'か', u'き', u'く', u'け', u'こ',
        u'さ', u'し', u'す', u'せ', u'そ', u'た', u'ち', u'つ', u'て', u'と',
        u'な', u'に', u'ぬ', u'ね', u'の', u'は', u'ひ', u'ふ', u'へ', u'ほ',
        u'ま', u'み', u'む', u'め', u'も', u'や', u'ゆ', u'よ', u'ら', u'り',
        u'る', u'れ', u'ろ', u'わ', u'を', u'ん',
        # Obsolete characters
        u'ゐ', u'ゑ',
        # Small characters
        u'ぁ', u'ぃ', u'ぅ', u'ぇ', u'ぉ', u'ゕ', u'ゖ'
    ],
    # Digraphs（yōon, 拗音・ようおん）
    'di': [
        u'きゃ', u'きゅ', u'きょ', u'しゃ', u'しゅ', u'しょ', u'ちゃ', u'ちゅ',
        u'ちょ', u'にゃ', u'にゅ', u'にょ', u'ひゃ', u'ひゅ', u'ひょ', u'みゃ',
        u'みゅ', u'みょ', u'りゃ', u'りゅ', u'りょ'
    ],
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
    'repeater_dakuten': u'ゞ',    # あひゞき = あひびき
    # Start and end positions in Unicode.
    'range': [0x3040, 0x309F]
}

# Katakana（片仮名・カタカナ）
# Range: U+30A1 - U+30FA
katakana_charset = {
    'type': KATAKANA,
    # Monographs（gojūon, 五十音・ごじゅうおん）
    'mono': [
        u'ア', u'イ', u'ウ', u'エ', u'オ', u'カ', u'キ', u'ク', u'ケ', u'コ',
        u'サ', u'シ', u'ス', u'セ', u'ソ', u'タ', u'チ', u'ツ', u'テ', u'ト',
        u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ', u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ',
        u'マ', u'ミ', u'ム', u'メ', u'モ', u'ヤ', u'ユ', u'ヨ', u'ラ', u'リ',
        u'ル', u'レ', u'ロ', u'ワ', u'ヲ', u'ン',
        # Obsolete characters
        u'ヰ', u'ヱ',
        # Small characters
        u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ', u'ヵ', u'ヶ'
    ],
    # Digraphs（yōon, 拗音・ようおん）
    'di': [
        u'キャ', u'キュ', u'キョ', u'シャ', u'シュ', u'ショ', u'チャ', u'チュ',
        u'チョ', u'ニャ', u'ニュ', u'ニョ', u'ヒャ', u'ヒュ', u'ヒョ', u'ミャ',
        u'ミュ', u'ミョ', u'リャ', u'リュ', u'リョ'
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
    'dbl_hyph': u'゠',
    # Start and end positions in Unicode.
    'range': [0x30A0, 0x30FF]
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

# For ease of processing, we're making some lookup tables between
# rōmaji, hiragana and katakana.

# Ordered lists of all characters in each script.
romaji_all = romaji_charset['mono'] + romaji_charset['di']
hiragana_all = hiragana_charset['mono'] + hiragana_charset['di']
katakana_all = katakana_charset['mono'] + katakana_charset['di']
romaji_charset['all'] = romaji_all
hiragana_charset['all'] = hiragana_all
katakana_charset['all'] = katakana_all

# Create a lookup table for rōmaji to kana.
romaji_charset['kana_lt'] = romaji_lt(romaji_all, hiragana_all, katakana_all)
from reisan.util.upprint import upprint
upprint(romaji_charset['kana_lt'])

# Generate lookup tables for looking up the vowels and consonants
# of each character set.
kana_vc_lt = generate_vc_lt(romaji_charset, hiragana_charset, katakana_charset)

# Generate lookup tables specifically for mapping kana characters
# to rōmaji equivalents, including geminate marker entries.
hiragana_romaji = zip_kana(romaji_charset, hiragana_charset, add_geminate=True)
katakana_romaji = zip_kana(romaji_charset, katakana_charset, add_geminate=True)

kana_scripts = {
    'hiragana': hiragana_charset,
    'katakana': katakana_charset
}
