"""
Utility functions.
"""

import re

NON_AZ_REGEXP = re.compile('[^a-z]')


def normalize(word):
    """
    Normalize a word by converting it to lower-case and
    removing all characters that are not 'a',...,'z'.

    @param word: Word to normalize
    @type word: str or unicode
    """
    return re.sub(NON_AZ_REGEXP, '', word.lower())
