KanaConverter
=============

Converts hiragana and katakana to rōmaji according to Modified Hepburn
transliteration rules.

The converter is built as a finite state machine and attempts to convert
any input to a sensible output even if character combinations are used
that don't normally occur in Japanese.

Example
-------

Some example conversions are listed below:

```python
from kanaconv import KanaConverter
conv = KanaConverter()

conv.to_romaji(u'がっこう')  # u'gakkō'
conv.to_romaji(u'セーラー')  # u'sērā'
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


Installing
----------

This package is [available on PyPI](https://pypi.python.org/pypi/repov/0.4):

    pip install repov

The source is [available on Github](https://github.com/msikma/repov).


Usage
-----

Import the module and run `repov.get_version()` to get started:

```python
import repov
version = repov.get_version()
print(version)  # e.g. master-27-7072898
```

In this example, we're on the master branch, the 27th commit, identified
by the short hash `7072898`.

You can pass a template to `get_version()` to get customized output. Use a
string as argument containing the variables you want in between % signs.
The default template is `%branch-any%-%count%-%hash%`. Any variable that
is for some reason unavailable will be replaced with `(unknown)`:

```python
repov.get_version('%branch%')       # master
repov.get_version('%branch-any%')   # (depends on situation, see below)
repov.get_version('%branch-all%')   # HEAD, origin/master, master
repov.get_version('%count%')        # 27
repov.get_version('%count-hex%')    # 1b
repov.get_version('%hash%')         # 7072898
repov.get_version('%hash-full%')    # 7072898a6a04f867c7d7b8a8aa4249a8d408bc0a
repov.get_version('%foobar%')       # (unknown)
```

The `%branch-any%` variable is the most versatile. The following is returned
depending on the situation:

* local branch: **master**
* remote tracking branch (in sync): **master**
* remote tracking branch (not in sync): **remotes/origin/feature-foo**
* tag: **v1.2.3**
* general detached head: **v1.0.6-5-g2393761**

If the `git` command itself is unusable for some reason, all variables
will become `(unknown)`.

### Advanced

To change the Git command:

```python
repov.Parser.git_cmd = '../../some/path/git'
```

To change the fallback string used for variables that couldn't be
computed:

```python
repov.Parser.unknown_segment = '(N/A)'  # default: '(unknown)'
```

You can also add your own Git commands to run using
`repoV.repov_parser.merge_git_args()`. See the included `defaults.py` file 
for an example of how to do this.


License
-------

MIT licensed.
