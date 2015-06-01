# coding=utf8
#
# Copyright (C) 2014-2015, Reisan Ltd. - All rights reserved.
# This file is proprietary and confidential. For more information,
# see the 'copyright.md' file, which is part of this source code package.

'''
These are the exceptions that may occur when using the kana converter module.
'''


class InvalidScriptError(Exception):
    '''
    Raised in case a kana translation is attempted without 'hiragana' or
    'katakana' as the target.
    '''
    pass
