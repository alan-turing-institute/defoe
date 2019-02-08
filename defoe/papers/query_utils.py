"""
Query-related utility functions.
"""

from defoe import query_utils

"""
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); (other value) original word. 

"""
prep_type= 1

def get_article_matches(issue, keywords):
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
    :type keywords: list(str or unicode:
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for article in issue:
            match = None
            for word in article.words:
                preprocessed_word = query_utils.preprocess_word(word, prep_type)
                if preprocessed_word == keyword:
                    match = (issue.date.date(), issue, article, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next article
    return matches


def get_article_keywords(article, keywords):
    """
    Gets list of keywords occuring within an article.

    Article words are normalized, by removing all non-'a-z|A-Z'
    characters.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: sorted list of keywords that occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, prep_type)
        if preprocessed_word in keywords:
            matches.add(preprocessed_word)
    return sorted(list(matches))


def article_contains_word(article, keyword):
    """
    Checks if a keyword occurs within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keyword
    :type keywords: str or unicode
    :return: True if the article contains the word, false otherwise
    :rtype: bool
    """
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, prep_type)
        if keyword == preprocessed_word:
            return True
    return False


def article_stop_words_removal(article):
    """
    Remove the stop words of an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :return: True article without stop words
    :rtype: list
    """

    stop_words = set(stopwords.words('english'))
    article_words = []
    for word in article.words:
        preprocessed_word = preprocessed_word(word, prep_type)
        if not preprocessed_word in stop_words:
           article_words.append(preprocessed_word)
    return article_words


