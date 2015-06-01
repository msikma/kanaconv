# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
Katakana values and lookup tables are defined here.
'''
import re
from kanaconv.constants import *
from kanaconv.utils import re_list
from kanaconv.charsets import katakana, hiragana, lvmarker


kana_re_lvm = re.escape(lvmarker)
kana_re_gem = '[%s]' % re_list([katakana['geminate'], hiragana['geminate']])
kana_re_xvowels = '[%s]' % re_list(katakana['set_e'], hiragana['set_e'])
kana_re_digraph = '[%s][%s]' % (re_list(katakana['set_c'], hiragana['set_c']),
                                re_list(katakana['set_d'], hiragana['set_d']))

from reisan.util.upprint import upprint
upprint(kana_re_lvm)
upprint(kana_re_gem)
upprint(kana_re_xvowels)
upprint(kana_re_digraph)

katakana_re_gem = re.escape(katakana['geminate'])
katakana_di_re_base = '[%s][%s]' % (re_list(katakana['set_c']),
                                    re_list(katakana['set_d']))

hiragana_re_gem = re.escape(hiragana['geminate'])
hiragana_di_re_base = '[%s][%s]' % (re_list(hiragana['set_c']),
                                    re_list(hiragana['set_d']))

# The following three regular expressions are used for matching
katakana_re = {
    'digraph': {
        'gem': re.compile(katakana_re_gem + katakana_di_re_base, re.UNICODE),
        'lvm': re.compile(katakana_di_re_base + re_lvm, re.UNICODE),
        'lvm_gem': re.compile(katakana_re_gem + katakana_di_re_base + re_lvm,
                              re.UNICODE)
    }
}
hiragana_re = {
    'digraph': {
        'gem': re.compile(hiragana_re_gem + hiragana_di_re_base, re.UNICODE),
        'lvm': re.compile(hiragana_di_re_base + re_lvm, re.UNICODE),
        'lvm_gem': re.compile(hiragana_re_gem + hiragana_di_re_base + re_lvm,
                              re.UNICODE)
    }
}

# Monographs（gojūon, 五十音・ごじュうおん）
