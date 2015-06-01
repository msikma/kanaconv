# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
test
'''



hiragana = [u'あ', u'い', u'う', u'え', u'お', u'か', u'き']
romaji = ('a', 'a'), ('ka', 'a', 'k'), ('ki', 'i', 'k'), ('ku', 'u', 'k')




a = u'スーピード'
b = u'スーーピード'

lt = [
    (u'スー', u'sū', u'ū'),
    (u'ピー', u'pī', u'ī'),
    (u'ス', u'su', u'u'),
    (u'ピ', u'pi', u'i'),
    (u'ド', u'do', u'o')
]
kana = [item[0] for item in lt]

import re
from reisan.util.upprint import upprint
split_re = r'(%s)' % '|'.join(map(re.escape, kana))
splitter = re.compile(split_re, re.UNICODE)

z = splitter.split(b)
upprint(z)

curr = None
for char in z:
    if char == '':
        continue
