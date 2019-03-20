"""
Query-related utility functions.
"""

from defoe import query_utils

"""
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); original word (3). 

"""
prep_type= 2

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
    Get list of keywords occuring within an article.

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
    Check if a keyword occurs within an article.

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

def get_article_as_string(article):
    """
    Return an article as a single string.

    :param article: Article
    :type article: defoe.papers.article.Article
    :return: The complete Article as a string
    :rtype: string
    """
    article_string=''
    for word in article.words:
        preprocessed_word = query_utils.preprocess_word(word, prep_type)
        if article_string == '' :
            article_string = preprocessed_word
        else:
            article_string+=' '+ preprocessed_word
    return article_string


def get_sentences_list_matches(article_string, keysentence):
    """
    Check which keysentences from occurs within the text of an article_string
    and return the list of matches.

    :param article_string: article_string
    :type article_string: string 
    :param keysentence: sentences
    :type: array of strings
    :return: The list of senteces matches
    :rtype: set of sentences
    """
    match=set()
    for sentence in keysentence:
        if sentence in article_string:
                    match.add(sentence)
    return sorted(list(match))

def get_article_idx(filename, article, keywords, ocr):
    """
    Gets a list of keywords (and their indices) within an article.

    Article words are preprocessed. 
    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: article
    :rtype article: defoe.papers.article.Article
    :return: sorted list of keywords and indices hat occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for idx, word in enumerate(article.words):
        preprocessed_word = query_utils.preprocess_word(word, prep_type)
        if preprocessed_word in keywords:
            match=(preprocessed_word, idx)
            matches.add(match)
    return article, filename, sorted(list(matches)),ocr


def get_concordance(article, filename, match, window, ocr):
    """
    For a given keyword (and its position in an article), it returns the concordance of words (before and after) using a window.
    :param article: Article
    :type article: defoe.papers.article.Article
    :parm match: keyword and its position inside the article list
    :type: list
    :window: number of words to the right and left
    :type: integer
    :return: keyword and its concordance
    :rtype: list
    """
    keyword = match[0]
    idx = match[1]
    article_size= len(article.words)
     
    if idx >=window: 
        start_idx= idx-window
    else: 
        start_idx=0

    if idx + window >=article_size:
        end_idx = article_size
    else:
	end_idx= idx + window + 1

    concordance_words = []
    for word in article.words[start_idx:end_idx]:
	concordance_words.append(query_utils.preprocess_word(word, prep_type))
    return (filename, keyword,concordance_words, ocr)
    
