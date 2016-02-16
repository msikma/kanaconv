# coding=utf8
#
# (C) 2015-2016, MIT License

'''
A list of exceptions that may be raised.
'''


class InvalidCharacterTypeError(Exception):
    '''
    A character can only be a consonant-vowel pair or a vowel.
    '''
    pass


class UnexpectedCharacterError(Exception):
    '''
    Found a character in the string that we can't deal with.
    '''
    pass
