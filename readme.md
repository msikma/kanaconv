KanaConverter
=============

Converts hiragana and katakana to rōmaji according to Modified Hepburn
transliteration rules.

The converter is built as a finite state machine and attempts to convert
any input to a sensible output even if character combinations are used
that don't normally occur in Japanese.

**Note, this package is not working properly yet. It's only at the initial few
commits.**


Example
-------

Some example conversions are listed below:

```python
from kanaconv import KanaConverter
conv = KanaConverter()

conv.to_romaji(u'がっこう') # u'gakkō'
conv.to_romaji(u'セーラー') # u'sērā'
conv.to_romaji(u'おねえさん') # u'onēsan'),
conv.to_romaji(u'こおり') # u'kōri'),
conv.to_romaji(u'スーパーマン') # u'sūpāman'),
conv.to_romaji(u'とうきょう') # u'tōkyō'),
conv.to_romaji(u'パーティー') # u'pātī'),
```


Support
-------

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


License
-------

MIT licensed.
