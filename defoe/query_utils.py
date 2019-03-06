"""
Query-related utility functions.
"""
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

NON_AZ_REGEXP = re.compile('[^a-z]')


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

def stemming(word):
    """
    Stemming is a process of reducing words to their word stem, 
    base or root form (for example, books — book, looked — look). 
    The main two algorithms are Porter stemming algorithm 
    (removes common morphological and inflexional endings from words - Used here),
     and Lancaster stemming algorithm (a more aggressive stemming algorithm). 

    :param word: Word to stemm
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """

    stemmer= PorterStemmer()
    return stemmer.stem(word)

def lemmatization(word):
    """
    The aim of lemmatization, like stemming, is to reduce inflectional forms to a common base form.
    As opposed to stemming, lemmatization does not simply chop off inflections. 
    Instead it uses lexical knowledge bases to get the correct base forms of words.


    :param word: Word to normalize
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    lemmatizer=WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

def preprocess_word(word, prep_type):
    """
    Preprocess a word by applying different treatments depending on the prep_type paramenter.
    (0) normalize; (1) normalize + stemming; (2) normalize + lemmatization; (3) orig word. 

    :param word: word
    :type word: string
    :param prep_type: 0 to apply just normalize. 1 to apply normalize and stemming, 2 to apply normalize and lemmatization, and 3 to return the original word.
    :type integer 
    :return: words
    :rtype: string
    """

    normalized_word = normalize(word)
    if prep_type == 0:
        preprocessed_word = normalized_word
    elif prep_type == 1:
       preprocessed_word = stemming(normalized_word)
    elif prep_type == 2:
       preprocessed_word = lemmatization(normalized_word)
    elif prep_type == 3:
       preprocessed_word = word
    return preprocessed_word



