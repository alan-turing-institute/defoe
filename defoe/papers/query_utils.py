"""
Query-related utility functions.
"""

from nltk.corpus import stopwords

from defoe import query_utils
from defoe.query_utils import PreprocessWordType


def get_article_matches(issue,
                        keywords,
                        preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Get articles within an issue that include one or more keywords.
    For each article that includes a specific keyword, add a tuple of
    form:

        (<DATE>, <ISSUE>, <ARTICLE>, <KEYWORD>)

    If a keyword occurs more than once in an article, there will be
    only one tuple for the article for that keyword.

    If more than one keyword occurs in an article, there will be one
    tuple per keyword.

    :param issue: issue
    :type issue: defoe.alto.issue.Issue
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for article in issue:
            match = None
            for word in article.words:
                preprocessed_word = query_utils.preprocess_word(
                    word,
                    preprocess_type)
                if preprocessed_word == keyword:
                    match = (issue.date.date(), issue, article, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next article
    return matches


def get_article_keywords(article,
                         keywords,
                         preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Get list of keywords occuring within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords that occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                        preprocess_type)
        if preprocessed_word in keywords:
            matches.add(preprocessed_word)
    return sorted(list(matches))


def article_contains_word(article,
                          keyword,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Check if a keyword occurs within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keyword
    :type keywords: str or unicode
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: True if the article contains the word, false otherwise
    :rtype: bool
    """
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                        preprocess_type)
        if keyword == preprocessed_word:
            return True
    return False


def article_stop_words_removal(article,
                               preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Remove the stop words of an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: article words without stop words
    :rtype: list(str or unicode)
    """
    stop_words = set(stopwords.words('english'))
    article_words = []
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word not in stop_words:
            article_words.append(preprocessed_word)
    return article_words


def get_article_as_string(article,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Return an article as a single string.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: article words as a string
    :rtype: string or unicode
    """
    article_string = ''
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if article_string == '':
            article_string = preprocessed_word
        else:
            article_string += (' ' + preprocessed_word)
    return article_string


def get_sentences_list_matches(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :param keysentence: sentences
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match = set()
    for sentence in keysentence:
        if sentence in text:
            match.add(sentence)
    return sorted(list(match))


def get_article_keyword_idx(article,
                            keywords,
                            preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Gets a list of keywords (and their position indices) within an
    article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords and their indices
    :rtype: list(tuple(str or unicode, int))
    """
    matches = set()
    for idx, word in enumerate(article.words):
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word in keywords:
            match = (preprocessed_word, idx)
            matches.add(match)
    return sorted(list(matches))


def get_concordance(article,
                    keyword,
                    idx,
                    window,
                    preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    For a given keyword (and its position in an article), return
    the concordance of words (before and after) using a window.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keyword: keyword
    :type keyword: str or unicode
    :param idx: keyword index (position) in list of article's words
    :type idx: int
    :window: number of words to the right and left
    :type: int
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: concordance
    :rtype: list(str or unicode)
    """
    article_size = len(article.words)

    if idx >= window:
        start_idx = idx - window
    else:
        start_idx = 0

    if idx + window >= article_size:
        end_idx = article_size
    else:
        end_idx = idx + window + 1

    concordance_words = []
    for word in article.words[start_idx:end_idx]:
        concordance_words.append(
            query_utils.preprocess_word(word, preprocess_type))
    return concordance_words
