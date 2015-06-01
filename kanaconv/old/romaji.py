# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
A set of functions to help clean up and normalize the rōmaji output.
'''
from kanaconv.constants import romaji_charset

macrons = romaji_charset['macrons']


def add_macrons(string):
    '''
    Adds macron characters to a string. For example, 'raamen' is changed
    into 'rāmen'.
    '''
    for char in macrons:
        string = string.replace(char, macrons[char])
    return string
