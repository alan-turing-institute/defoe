"""
Query-related utility functions.
"""

from defoe import query_utils


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
                if query_utils.normalize(word) == keyword:
                    match = (issue.date.date(), issue, article, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next article
    return matches


def get_keywords_in_article(article, keywords):
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
    matches = []
    for word in article.words:
        normalized_word = query_utils.normalize(word)
        if normalized_word in keywords:
            matches.append(normalized_word)
    return sorted(list(set(matches)))


def word_article_count_list_to_dict(word_counts):
    """
    Converts list of list of words and numbers of articles these occur
    in into list of dictionaries of words and numbers.

    Dictionary is of form:

        {
            "words": "<WORD>, <WORD>, ...",
            "count": <COUNT>
        }

    :param word_counts: words and counts
    :type word_counts: list(tuple(int, str or unicode))
    :return: dict
    :rtype: dict
    """
    result = []
    for word_count in word_counts:
        result.append({"words": word_count[0],
                       "count": word_count[1]})
    return result


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
        normalized_word = query_utils.normalize(word)
        if keyword == normalized_word:
            return True
    return False
