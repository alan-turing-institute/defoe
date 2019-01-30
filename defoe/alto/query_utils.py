"""
Query-related utility functions.
"""

from defoe import query_utils


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
                continue # move to next page
    return matches
