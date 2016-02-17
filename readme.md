KanaConv
========

**Converts hiragana and katakana to rōmaji according to Modified Hepburn
transliteration rules.**

<p align="center">
とうきょう → tōkyō　　パーティー → pātī
</p>

For a full overview of the rules by which this module operates, see [the
Wikipedia page on Hepburn romanization](https://en.wikipedia
.org/wiki/Hepburn_romanization). In addition to Modified Hepburn, this module
implements a commonsense way to handle some rare and uncommon edge cases
(with some limitations; see below).

The converter attempts to produce sensible output even when given unusual
character combinations that don't normally occur in dictionary words.

Compatible with Python 2.7 and 3.4.


Installation and usage
----------------------

The easiest way to install this module is by using `pip`, e.g.:

    $ pip install kanaconv
This will allow you to use the command line utility:

```
$ kanaconv ウェスト
wesuto
$ kanaconv スーパーマン
sūpāman
$ kanaconv がっこう
gakkō
```

If you're developing an application, the converter is available
through `kanaconv.KanaConv`.

```python
from kanaconv import KanaConv
conv = KanaConv()

conv.to_romaji('スーパーマン')　 # u'sūpāman'
conv.to_romaji('こおり')　　　　 # u'kōri'
conv.to_romaji('おねえさん')　　 # u'onēsan'
conv.to_romaji('とうきょう')　　 # u'tōkyō'
conv.to_romaji('パーティー')　　 # u'pātī'
conv.to_romaji('ぬれ|えん')　　　# u'nureen' (濡れ縁; see section on word borders)
```

Note: just use `u'カタカナ'` when working with Python 2.7.


Transliteration support
-----------------------

Aside from basic hiragana and katakana, the following characters are supported:

* The wi/we kana characters（ゐゑ・ヰヱ）
* Rare characters that are mostly for loanwords (ヺヸヷヴゔ)
* The repeater characters（ゝゞヽヾ）
* The yori and koto ligatures（ゟ・ヿ）
* Numerous punctuation and bracket characters (e.g. 【】「」・。, etc)

Conversely, the following characters and features are not supported,
with no plans to support them in the future unless they are requested
with a real-life use case:

* Half width katakana (U+FF65 - U+FF9F)
* Enclosed katakana (U+32D0 - U+32FE)
* Katakana phonetic extensions (U+31F0 - U+31FF)
* Historical kana supplement (U+1B000, U+1B001)
* "Here" sign (🈁; U+1F201)
* "Service" sign (🈂; U+1F202)
* "Data" sign (🈓; U+1F213)
* Rare typographical symbols
* Vertical-only symbols

### Word borders

Generally, combinations such as *o + u* are transliterated with a macron
character, e.g. *ō*. This is not the case when there is a word border
between the two vowels.

For example, the word 子（こ）馬（うま）has the *o + u* vowels split across
two separate words. Hence, no long vowel is pronounced, and the correct
transliteration is *kouma*.

Since the module does not have an internal dictionary, it can't know that
こうま is split across two words in such a way. In order to get a correct
transliteration, you need to manually add a pipe character to the input
to indicate the border, e.g. こ|うま:

```python
# transliteration of 子馬
conv.to_romaji(u'こうま')　　　　 # u'kōma'  - incorrect
conv.to_romaji(u'こ|うま')　　　　# u'kouma' - correct
```

This rule applies to the combinations *a + a*, *u + u*, *e + e*, *o + o*,
and *o + u*. The *i + i* combination is written as *ii*, but an extended
vowel due to a long vowel marker is written as *ī*. All other combinations
of vowels are always written separately.

### Unicode blocks

The following full Unicode blocks are supported in this module:

**<p align="center">
Katakana Unicode Block
</p>**
<p align="center">
　　　　　　　０　１　２　３　４　５　６　７　８　９　Ａ　Ｂ　Ｃ　Ｄ　Ｅ　Ｆ<br />
Ｕ＋３０Ａｘ　゠　ァ　ア　ィ　イ　ゥ　ウ　ェ　エ　ォ　オ　カ　ガ　キ　ギ　ク<br />
Ｕ＋３０Ｂｘ　グ　ケ　ゲ　コ　ゴ　サ　ザ　シ　ジ　ス　ズ　セ　ゼ　ソ　ゾ　タ<br />
Ｕ＋３０Ｃｘ　ダ　チ　ヂ　ッ　ツ　ヅ　テ　デ　ト　ド　ナ　ニ　ヌ　ネ　ノ　ハ<br />
Ｕ＋３０Ｄｘ　バ　パ　ヒ　ビ　ピ　フ　ブ　プ　ヘ　ベ　ペ　ホ　ボ　ポ　マ　ミ<br />
Ｕ＋３０Ｅｘ　ム　メ　モ　ャ　ヤ　ュ　ユ　ョ　ヨ　ラ　リ　ル　レ　ロ　ヮ　ワ<br />
Ｕ＋３０Ｆｘ　ヰ　ヱ　ヲ　ン　ヴ　ヵ　ヶ　ヷ　ヸ　ヹ　ヺ　・　ー　ヽ　ヾ　ヿ<br />
</p>

**<p align="center">
Hiragana Unicode Block
</p>**
<p align="center">
　　　　　　　０　１　２　３　４　５　６　７　８　９　Ａ　Ｂ　Ｃ　Ｄ　Ｅ　Ｆ<br />
Ｕ＋３０４ｘ　　　ぁ　あ　ぃ　い　ぅ　う　ぇ　え　ぉ　お　か　が　き　ぎ　く<br />
Ｕ＋３０５ｘ　ぐ　け　げ　こ　ご　さ　ざ　し　じ　す　ず　せ　ぜ　そ　ぞ　た<br />
Ｕ＋３０６ｘ　だ　ち　ぢ　っ　つ　づ　て　で　と　ど　な　に　ぬ　ね　の　は<br />
Ｕ＋３０７ｘ　ば　ぱ　ひ　び　ぴ　ふ　ぶ　ぷ　へ　べ　ぺ　ほ　ぼ　ぽ　ま　み<br />
Ｕ＋３０８ｘ　む　め　も　ゃ　や　ゅ　ゆ　ょ　よ　ら　り　る　れ　ろ　ゎ　わ<br />
Ｕ＋３０９ｘ　ゐ　ゑ　を　ん　ゔ　ゕ　ゖ　　　　　゙　゚　゛　゜　ゝ　ゞ　ゟ<br />
</p>

</p>

There are a number of other blocks for e.g. half-width characters and other
rare glyphs, but none of them are supported.

More info on the supported typographic symbols can be found
[on the Wikipedia page for Japanese typographic symbols](https://en.wikipedia.org/wiki/Japanese_typographic_symbols).

### Existing English terms

A lot of katakana loan words have English equivalents, but this module will
only return transliterated rōmaji. For example, パーティー is transliterated to
"pātī", whereas the English term is "party".

The use of an internal dictionary to handle these word replacements is
considered to be out of scope for this project. Additionally, proper names
like Tōkyō are not capitalized for the same reason.

### Limitations (unusual combinations and edge cases)

This module will attempt to create sensible output even in the case of
unusual character combinations that normally don't occur in a dictionary.
However, there's a limit to what we can infer from the kana alone.

A number of cases are ambiguous, or can have a different preferred
romanization based on the word. They're sufficiently rare (most of these
have practically zero usage in dictionary words) that we've settled on a
single implementation.

* ウォ is transliterated as 'wo', though it can represent 'vo' in rare words
* ヴィ and ヸ are transliterated as 'vi', but could also be 'wi'
* クヮ is transliterated as 'kuwa', though 'kwa' is also possible; in general,
  ヮ behaves exactly like ワ
* ゑ and ヱ are technically 'we', sometimes 'ye', but are pronounced and
  transliterated as 'e'
* ゐ is technically 'wi', but is pronounced and transliterated as 'i'
* ヰ can be 'i', 'wi' or 'vi' depending on the word; we've settled on 'i'
  in all cases
* ゖ could theoretically be 'ke' in online speech, but it's the (nearly unused)
  hiragana version of ヶ which is always 'ka', so it's considered 'ka' here
  too

If these behaviors need to be changed as per a real life example, feel free
to send in a comment or a PR.


Development
-----------

I'm always glad to accept pull requests or to look at issues or questions.

### Tests

Run `./setup.py test` to run the unit tests. An additional speed test
is included as well, which you can run with
`python -m kanaconv.tests.test_speed`.


License
-------

MIT licensed.
