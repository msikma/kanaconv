#!/usr/bin/env python
# coding=utf8
#
# (C) 2015-2016, MIT License

'''
Installation configuration.
'''
from setuptools import setup

setup(
    name='kanaconv',
    version='1.0.0',
    description='Converts hiragana and katakana to rōmaji according to '
                'Modified Hepburn transliteration rules',
    author='Michiel Sikma',
    author_email='michiel@sikma.org',
    license='MIT',
    test_suite='kanaconv.tests.test_kanaconv',
    packages=['kanaconv'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    entry_points={
        'console_scripts': [
            'kanaconv=kanaconv.cli.kanaconv:main'
        ]
    },
    zip_safe=False
)
