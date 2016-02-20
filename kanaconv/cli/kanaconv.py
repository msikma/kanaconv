#!/usr/bin/env python
# coding=utf8
#
# (C) 2015-2016, MIT License

'''
Command-line helper tool to do kana conversions.
'''
import sys
import argparse
import pkg_resources
from ..converter import KanaConv
from ..constants import CIRCUMFLEX_STYLE

PACKAGE = pkg_resources.require('kanaconv')[0]
PYTHON_2 = sys.version_info < (3, 0)


def main():
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.description = '''\
Converts hiragana and katakana to rōmaji according to Modified Hepburn \
transliteration rules.
'''
    argparser.epilog = '''\
See <{}> for more information.
    '''.format('https://github.com/msikma/kanaconv')
    argparser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help message and exit.'
    )
    argparser.add_argument(
        '-V', '--version',
        action='version', version='{} ({})'.format(
            PACKAGE.project_name,
            PACKAGE.version
        ),
        help='Show version number and exit.'
    )
    argparser.add_argument(
        '--circumflex',
        action='store_true',
        help='Whether to use circumflex (â) accents instead of '
             'the default macron (ā).'
    )
    argparser.add_argument(
        '--uppercase',
        action='store_true',
        help='Changes the output to uppercase.'
    )
    argparser.add_argument(
        'str',
        help='String to transliterate.'
    )
    args = argparser.parse_args()

    conv = KanaConv()

    if args.circumflex:
        conv.set_vowel_style(CIRCUMFLEX_STYLE)

    if args.uppercase:
        conv.set_uppercase(True)

    if not PYTHON_2:
        input_str = args.str
    else:
        input_str = args.str.decode('utf-8')

    print(conv.to_romaji(input_str))
