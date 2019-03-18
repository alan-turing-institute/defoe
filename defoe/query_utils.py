"""
Query-related utility functions and types.
"""

import os
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


def parse_preprocess_word_type(type_str):
    """
    Parse a string into a PreprocessWordType.

    :param type_str: One of none|normalize|stem|lemmatize
    :type type_str: str or unicode
    :return: word preprocessing type
    :rtype: PreprocessingWordType
    :raises: ValueError if "preprocess" is not one of the expected
    values
    """
    try:
        preprocess_type = PreprocessWordType[type_str.upper()]
    except KeyError:
        raise KeyError("preprocess must be one of {} but is '{}'"
                       .format([k.lower() for k in list(
                           PreprocessWordType.__members__.keys())],
                               type_str))
    return preprocess_type


def extract_preprocess_word_type(config,
                                 default=PreprocessWordType.LEMMATIZE):
    """
    Extract PreprocessWordType from "preprocess" dictionary value in
    query configuration.

    :param config: config
    :type config: dict
    :param default: default value if "preprocess" is not found
    :type default: PreprocessingWordType
    :return: word preprocessing type
    :rtype: PreprocessingWordType
    :raises: ValueError if "preprocess" is not one of
    none|normalize|stem|lemmatize
    """
    if "preprocess" not in config:
        preprocess_type = default
    else:
        preprocess_type = parse_preprocess_word_type(config["preprocess"])
    return preprocess_type


def extract_data_file(config, default_path):
    """
    Extract data file path from "data" dictionary value in query
    configuration.

    :param config: config
    :type config: dict
    :param default_path: default path to prepend to data file path if
    data file path is a relative path
    :type default_path: str or unicode
    :return: file path
    :rtype: str or unicode
    :raises: KeyError if "data" is not in config
    """
    data_file = config["data"]
    if not os.path.isabs(data_file):
        data_file = os.path.join(default_path, data_file)
    return data_file


def extract_window_size(config, default=10):
    """
    Extract window size from "window" dictionary value in query
    configuration.

    :param config: config
    :type config: dict
    :param default: default value if "window" is not found
    :type default: int
    :return: window size
    :rtype: int
    :raises: ValueError if "window" is >= 1
    """
    if "window" not in config:
        window = default
    else:
        window = config["window"]
    if window < 1:
        raise ValueError('window must be at least 1')
    return window


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
