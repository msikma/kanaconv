KanaConv
========

**Converts hiragana and katakana to rōmaji according to Modified Hepburn
transliteration rules.**

<p align="center">
とうきょう → tōkyō　　パーティー → pātī
</p>

For a full overview of the rules by which this module operates, see [the
Wikipedia page on Hepburn romanization](https://en.wikipedia
.org/wiki/Hepburn_romanization).

The converter is built as a finite state machine and attempts to convert
any input to a sensible output even if character combinations are used
that don't normally occur in Japanese.

**Note, this package is not working properly yet. It's only at the initial few
commits.**


Example
-------

Some example conversions are listed below:

```python
from kanaconv import KanaConv
conv = KanaConv()

conv.to_romaji(u'がっこう')　　　 # u'gakkō'
conv.to_romaji(u'セーラー')　　　 # u'sērā'
conv.to_romaji(u'おねえさん')　　 # u'onēsan',
conv.to_romaji(u'こおり')　　　　 # u'kōri',
conv.to_romaji(u'スーパーマン')　 # u'sūpāman'
conv.to_romaji(u'とうきょう')　　 # u'tōkyō'
conv.to_romaji(u'パーティー')　　 # u'pātī'
conv.to_romaji(u'ぬれ|えん')　　　# u'nureen' (see section on word borders)
```


Transliteration support
-----------------------

Aside from basic hiragana and katakana, the following characters are supported:

* The wi/we kana characters（ゐゑ・ヰヱ）
* The repeater characters（ゝゞヽヾ）
* The koto ligature（ヿ）
* Small ka (ゕ; U+3095, and ヵ; U+30F5)
* Small ke (ゖ; U+3096, and ヶ; U+30F6)
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
transliteration, you need to manually add a pipe character to the input,
e.g. こ|うま:

```python
# transliteration of 子馬
conv.to_romaji(u'こうま')　　　　 # u'kōma'  - incorrect
conv.to_romaji(u'こ|うま')　　　　# u'kouma' - correct
```

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
[on the Wikipedia page for Japanese typographic symbols](https://en.wikipedia
.org/wiki/Japanese_typographic_symbols).

### Existing English terms

A lot of katakana loan words have English equivalents, but this module will
only return transliterated rōmaji. For example, パーティー is transliterated to
"pātī", whereas the English term is "party".

The use of an internal dictionary to handle these word replacements is
considered to be out of scope for this project. Additionally, proper names
like Tōkyō are not capitalized for the same reason.


License
-------

MIT licensed.
