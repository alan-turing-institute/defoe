"""
Query-related utility functions and types.
"""

import re
import enum
from nltk.stem import PorterStemmer, WordNetLemmatizer

NON_AZ_REGEXP = re.compile('[^a-z]')


class PreprocessWordType(enum.Enum):
    """
    Word preprocessing types.
    """
    NORMALIZE = 1
    """ Normalize word """
    STEM = 2
    """ Normalize and stem word """
    LEMMATIZE = 3
    """ Normalize and lemmatize word """
    NONE = 4
    """ Apply no preprocessing """


def normalize(word):
    """
    Normalize a word by converting it to lower-case and removing all
    characters that are not 'a',...,'z'.

    :param word: Word to normalize
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    return re.sub(NON_AZ_REGEXP, '', word.lower())


def stem(word):
    """
    Reducing word to its word stem, base or root form (for example,
    books - book, looked - look). The main two algorithms are:

    - Porter stemming algorithm: removes common morphological and
      inflexional endings from words, used here
      (nltk.stem.PorterStemmer).
    - Lancaster stemming algorithm: a more aggressive stemming
      algorithm.

    Like lemmatization, stemming reduces inflectional forms to a
    common base form. As opposed to lemmatization, stemming simply
    chops off inflections.

    :param word: Word to stemm
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    stemmer = PorterStemmer()
    return stemmer.stem(word)


def lemmatize(word):
    """
    Lemmatize a word, using a lexical knowledge bases to get the
    correct base forms of a word.

    Like stemming, lemmatization reduces inflectional forms to a
    common base form. As opposed to stemming, lemmatization does not
    simply chop off inflections. Instead it uses lexical knowledge
    bases to get the correct base forms of words.

    :param word: Word to normalize
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)


def preprocess_word(word, preprocess_type=PreprocessWordType.NONE):
    """
    Preprocess a word by applying different treatments
    e.g. normalization, stemming, lemmatization.

    :param word: word
    :type word: string or unicode
    :param preprocess_type: normalize, normalize and stem, normalize
    and lemmatize, none (default)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: preprocessed word
    :rtype: string or unicode
    """
    if preprocess_type == PreprocessWordType.NORMALIZE:
        normalized_word = normalize(word)
        preprocessed_word = normalized_word
    elif preprocess_type == PreprocessWordType.STEM:
        normalized_word = normalize(word)
        preprocessed_word = stem(normalized_word)
    elif preprocess_type == PreprocessWordType.LEMMATIZE:
        normalized_word = normalize(word)
        preprocessed_word = lemmatize(normalized_word)
    else:  # PreprocessWordType.NONE or unknown
        preprocessed_word = word
    return preprocessed_word
