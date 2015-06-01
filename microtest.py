# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

from kanaconv.converter import KanaConverter
conv = KanaConverter()
tests = [
    (u'メロディー', u'merodī'),
    (u'セーラー', u'sērā'),
    (u'ぬれ|えん', u'nureen')
]
for test in tests:
    input = test[0]
    expected = test[1]
    output = conv.to_romaji(input)
    does_it_pass = 'PASS' if expected == output else 'FAIL'
    print('test %s, got: %s, expected: %s (%s)' % (input, output, expected,
                                                   does_it_pass))
