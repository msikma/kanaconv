#!/usr/bin/env python
# coding=utf8
#
# (C) 2015, MIT License

from kanaconv.converter import KanaConv
conv = KanaConv()
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
