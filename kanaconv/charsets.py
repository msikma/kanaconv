# coding=utf8
#
# (C) 2015, MIT License

'''
The kana constants are defined here. This includes all hiragana and katakana
characters (as defined in several sets based on their processing needs),
as well as punctuation and other special characters, and their rōmaji
equivalents.

Additionally, read the comments in this file for information on what these
characters mean and how they're meant to be used.

Unicode ranges in this file are inclusive ranges.
'''
from kanaconv.constants import KATAKANA, HIRAGANA, ROMAJI
from kanaconv.utils import switch_charset

# For ease of processing, we've divided the kana characters into five sets.
#
# Each of these sets has its own processing needs. Both of these sets
# has a katakana and a hiragana version.

# Katakana（片仮名・カタカナ）
# Range: U+30A1 - U+30FA
katakana = {
    'type': KATAKANA,
    # Characters with one consonant and one vowel
    'set_cvs': [
        u'カ', u'キ', u'ク', u'ケ', u'コ',
        u'サ', u'シ', u'ス', u'セ', u'ソ',
        u'タ', u'チ', u'ツ', u'テ', u'ト',
        u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ',
        u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ',
        u'マ', u'ミ', u'ム', u'メ', u'モ',
        u'ヤ', u'ユ', u'ヨ',
        u'ラ', u'リ', u'ル', u'レ', u'ロ',
        u'ワ', u'ヲ',
        u'ヰ', u'ヱ', u'ン', u'ヵ', u'ヶ',
        # Characters with (han)dakuten
        u'ガ', u'ギ', u'グ', u'ゲ', u'ゴ',
        u'ザ', u'ジ', u'ズ', u'ゼ', u'ゾ',
        u'ダ', u'ヂ', u'ヅ', u'デ', u'ド',
        u'バ', u'ビ', u'ブ', u'ベ', u'ボ',
        u'パ', u'ピ', u'プ', u'ペ', u'ポ'
    ],
    # Regular vowels
    'set_vowels': [
        u'ア', u'イ', u'ウ', u'エ', u'オ'
    ],
    # Small vowel markers
    'set_xvowels': [
        u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ'
    ],
    # First characters of digraphs
    'set_digraphs_a': [
        u'キ', u'シ', u'チ', u'ヒ', u'ミ', u'リ', u'ナ'
        u'ギ', u'ジ', u'ヂ', u'ビ', u'ミ', u'リ', u'ピ'
    ],
    # Second characters of digraphs
    'set_digraphs_b': [
        u'ャ', u'ュ', u'ョ'
    ],
    # Geminate consonant marker（sukuon, 促音・そくおん）
    'geminate': u'ッ',
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
    'set_cvs': switch_charset(katakana['set_cvs'], HIRAGANA),
    'set_vowels': switch_charset(katakana['set_vowels'], HIRAGANA),
    'set_xvowels': switch_charset(katakana['set_xvowels'], HIRAGANA),
    'set_digraphs_a': switch_charset(katakana['set_digraphs_a'], HIRAGANA),
    'set_digraphs_b': switch_charset(katakana['set_digraphs_b'], HIRAGANA),
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
romaji = {
    'type': ROMAJI,
    # Characters with one consonant and one vowel
    # Each entry contains four strings:
    #
    #    1) the plain character;
    #    2) the added consonant in case of a geminate marker prefix;
    #    3) the consonant-only part of the character;
    #    4) the vowel;
    #    5) the long version of the vowel.
    #
    # They're used in the following ways, e.g. for チ ('chi', 't', 'ch', u'ī'):
    #
    #    チ　　　　[0]               chi
    #    ッチ　　　[1] + [0]         tchi
    #    チャ　　　[2] + [x]         cha (plus a vowel from the ャ character)
    #    ッチャ　　[1] + [2] + [x]   tcha
    #    ッチー　　[1] + [2] + [4]   tchī
    #
    # The macron characters āīūēō are used for long vowels. The same order
    # is used as for the katakana and hiragana lists.
    #
    # The 'n' is a special case, and it's kept here for ease of processing.
    'set_cvs': [
        ('ka', 'k', 'k', 'a', u'ā'), ('ki', 'k', 'k', 'i', u'ī'),
        ('ku', 'k', 'k', 'u', u'ū'), ('ke', 'k', 'k', 'e', u'ē'),
        ('ko', 'k', 'k', 'o', u'ō'), ('sa', 's', 's', 'a', u'ā'),
        ('shi', 's', 'sh', 'i', u'ī'), ('su', 's', 's', 'u', u'ū'),
        ('se', 's', 's', 'e', u'ē'), ('so', 's', 's', 'o', u'ō'),
        ('ta', 't', 't', 'a', u'ā'), ('chi', 't', 'ch', 'i', u'ī'),
        ('tsu', 't', 'ts', 'u', u'ū'), ('te', 't', 't', 'e', u'ē'),
        ('to', 't', 't', 'o', u'ō'), ('na', 'n', 'n', 'a', u'ā'),
        ('ni', 'n', 'n', 'i', u'ī'), ('nu', 'n', 'n', 'u', u'ū'),
        ('ne', 'n', 'n', 'e', u'ē'), ('no', 'n', 'n', 'o', u'ō'),
        ('ha', 'h', 'h', 'a', u'ā'), ('hi', 'h', 'h', 'i', u'ī'),
        ('fu', 'f', 'f', 'u', u'ū'), ('he', 'h', 'h', 'e', u'ē'),
        ('ho', 'h', 'h', 'o', u'ō'), ('ma', 'm', 'm', 'a', u'ā'),
        ('mi', 'm', 'm', 'i', u'ī'), ('mu', 'm', 'm', 'u', u'ū'),
        ('me', 'm', 'm', 'e', u'ē'), ('mo', 'm', 'm', 'o', u'ō'),
        ('ya', 'y', 'y', 'a', u'ā'), ('yu', 'y', 'y', 'u', u'ū'),
        ('yo', 'y', 'y', 'o', u'ō'), ('ra', 'r', 'r', 'a', u'ā'),
        ('ri', 'r', 'r', 'i', u'ī'), ('ru', 'r', 'r', 'u', u'ū'),
        ('re', 'r', 'r', 'e', u'ē'), ('ro', 'r', 'r', 'o', u'ō'),
        ('wa', 'w', 'w', 'a', u'ā'), ('wo', 'w', 'w', 'o', u'ō'),
        ('wi', 'w', 'w', 'i', u'ī'), ('we', 'w', 'w', 'e', u'ē'),
        ('n', 'n', 'n', 'n', 'n'), ('ka', 'k', 'k', 'a', u'ā'),
        ('ka', 'k', 'k', 'a', u'ā'), ('ga', 'g', 'g', 'a', u'ā'),
        ('gi', 'g', 'g', 'i', u'ī'), ('gu', 'g', 'g', 'u', u'ū'),
        ('ge', 'g', 'g', 'e', u'ē'), ('go', 'g', 'g', 'o', u'ō'),
        ('za', 'z', 'z', 'a', u'ā'), ('ji', 'j', 'j', 'i', u'ī'),
        ('zu', 'z', 'z', 'u', u'ū'), ('ze', 'z', 'z', 'e', u'ē'),
        ('zo', 'z', 'z', 'o', u'ō'), ('da', 'd', 'd', 'a', u'ā'),
        ('ji', 'j', 'j', 'i', u'ī'), ('zu', 'z', 'z', 'u', u'ū'),
        ('de', 'd', 'd', 'e', u'ē'), ('do', 'd', 'd', 'o', u'ō'),
        ('ba', 'b', 'b', 'a', u'ā'), ('bi', 'b', 'b', 'i', u'ī'),
        ('bu', 'b', 'b', 'u', u'ū'), ('be', 'b', 'b', 'e', u'ē'),
        ('bo', 'b', 'b', 'o', u'ō'), ('pa', 'p', 'p', 'a', u'ā'),
        ('pi', 'p', 'p', 'i', u'ī'), ('pu', 'p', 'p', 'u', u'ū'),
        ('pe', 'p', 'p', 'e', u'ē'), ('po', 'p', 'p', 'o', u'ō')
    ],
    # Regular vowels
    'set_vowels': [
        ('a', u'ā'), ('i', u'ī'), ('u', u'ū'), ('e', u'ē'), ('o', u'ō')
    ],
    # Small vowel markers
    'set_xvowels': [
        ('a', u'ā'), ('i', u'ī'), ('u', u'ū'), ('e', u'ē'), ('o', u'ō')
    ],
    # Replacement character for impossible geminate marker combinations
    'repl_char': '-',
    # First characters of digraphs (only the consonants are needed)
    # todo: implement
    'set_digraphs_a': [
        'ky', 'sh', 'ch', 'hy', 'my', 'ry', 'ny'
        'gy', 'j', 'dy', 'by', 'my', 'ry', 'py'
    ],
    # Second characters of digraphs
    'set_digraphs_b': [
        ('a', u'ā'), ('u', u'ū'), ('o', u'ō')
    ]
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
lvmarker = u'ー'
