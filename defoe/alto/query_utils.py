"""
Query-related utility functions.
"""

from defoe import query_utils
from defoe.query_utils import PreprocessWordType


def get_page_matches(document,
                     keywords,
                     preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<YEAR>, <DOCUMENT>, <PAGE>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :param document: document
    :type document: defoe.alto.document.Document
    :param keywords: keywords
    :type keywords: list(str or unicode:
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for page in document:
            match = None
            for word in page.words:
                preprocessed_word = query_utils.preprocess_word(
                    word, preprocess_type)
                if preprocessed_word == keyword:
                    match = (document.year, document, page, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next page
    return matches


def get_document_keywords(document,
                          keywords,
                          preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets list of keywords occuring within an document.

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
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if preprocessed_word in keywords:
                matches.add(preprocessed_word)
    return sorted(list(matches))


def document_contains_word(document,
                           keyword,
                           preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Checks if a keyword occurs within an article.

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
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if keyword == preprocessed_word:
                return True
    return False


def get_page_idx(page, 
                 keywords,
                 preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets a list of keywords (and their indices) within an page.
    Page words are preprocessed. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: page
    :rtype page: defoe.papers.page.Page
    :return: sorted list of keywords and indices hat occur within page
    :rtype: list(str or unicode)
    """
    matches = set()
    for idx, word in enumerate(page.words):
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word in keywords:
            match=(preprocessed_word, idx)
            matches.add(match)
    return page, sorted(list(matches))


def get_concordance(page, 
                    match, 
                    window,
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given keyword (and its position in an page), it returns the concordance of words (before and after) using a window.
    :param page: Page
    :type page: defoe.alto.page.Page
    :parm match: keyword and its position inside the page list
    :type: list
    :window: number of words to the right and left
    :type: integer
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: keyword and its concordance
    :rtype: list
    """
    keyword = match[0]
    idx = match[1]
    page_size= len(page.words)
     
    if idx >=window: 
        start_idx= idx-window
    else: 
        start_idx=0

    if idx + window >=page_size:
        end_idx = page_size
    else:
	end_idx= idx + window + 1
    
    prep_types =[]
    prep_t=["NORMALIZE", "STEM", "LEMMATIZE", "NONE"]
    for i in prep_t:
        concordance_words = []
        preprocess_type = PreprocessWordType[i]
        concordance_words.append("Preprocess Type: "+ str(preprocess_type))
        for word in page.words[start_idx:end_idx]:
	    concordance_words.append(query_utils.preprocess_word(word, preprocess_type))
        prep_types.append(concordance_words)
    return (keyword,prep_types)

def get_page_sentences(page, 
                 keywords,
                 preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets a list of keywords (and their indices) within an page.
    Page words are preprocessed. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: page
    :rtype page: defoe.papers.page.Page
    :return: sorted list of keywords and indices hat occur within page
    :rtype: list(str or unicode)
    """
    matches = set()
    page_string=""
    for word in page.words:
        page_string=page_string + " " + word
    page_sentences= query_utils.sentence_spliter(page_string)
    for sentence in page_sentences:
        try:
            sentence_token=query_utils.word_to_token(sentence)
            for token in sentence_token:
                preprocess_word=query_utils.preprocess_word(token,PreprocessWordType.NORMALIZE)
                if preprocess_word in keywords:
                    match=(preprocess_word, sentence)
                    matches.add(match)
        except:
            pass
    return page, sorted(list(matches))


def get_sentence_concordance(match, 
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given keyword (and its position in an page), it returns the concordance of words (before and after) using a window.
    :parm match: keyword and sentencet
    :type: list
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: keyword and its concordance
    :rtype: list
    """
    keyword = match[0]
    prep_types =[]
    prep_t=["NORMALIZE", "STEM", "LEMMATIZE", "NONE"]
    for i in prep_t:
        concordance_words = []
        preprocess_type = PreprocessWordType[i]
        concordance_words.append("Preprocess Type: "+ str(preprocess_type))
        sentence_token=query_utils.word_to_token(match[1])
        for word in sentence_token:
	    concordance_words.append(query_utils.preprocess_word(word, preprocess_type))
        prep_types.append(concordance_words)
    return (keyword,prep_types)

