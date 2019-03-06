"""
Query-related utility functions.
"""

from defoe import query_utils

"""
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); original word (3). 
"""
prep_type= 0

def get_page_matches(document, keywords):
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
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    for keyword in keywords:
        for page in document:
            match = None
            for word in page.words:
                if query_utils.normalize(word) == keyword:
                    match = (document.year, document, page, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next page
    return matches

def get_page_idx(page, keywords):
    """
    Gets a list of keywords (and their indices) within an page.
    Page words are preprocessed. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :return: page
    :rtype page: defoe.papers.page.Page
    :return: sorted list of keywords and indices hat occur within page
    :rtype: list(str or unicode)
    """
    matches = set()
    for idx, word in enumerate(page.words):
        preprocessed_word = query_utils.preprocess_word(word, prep_type)
        if preprocessed_word in keywords:
            match=(preprocessed_word, idx)
            matches.add(match)
    return page, sorted(list(matches))


def get_concordance(page, match, window):
    """
    For a given keyword (and its position in an page), it returns the concordance of words (before and after) using a window.
    :param page: Page
    :type page: defoe.alto.page.Page
    :parm match: keyword and its position inside the page list
    :type: list
    :window: number of words to the right and left
    :type: integer
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

    concordance_words = []
    for word in page.words[start_idx:end_idx]:
	concordance_words.append(query_utils.preprocess_word(word, prep_type))
    return (keyword,concordance_words)

