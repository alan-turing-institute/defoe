"""
Given a filename create a defoe.nzpp.articles.Articles.
"""

from defoe.nzpp.articles import Articles


def filename_to_object(filename):
    """
    Given a filename create a defoe.nzpp.articles.Articles. If an
    error arises during its creation this is caught and returned as a
    string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Articles, None) or (filename, error message),
    if there was an error creating Articles
    :rtype: tuple(defoe.nzpp.articles.Articles | str or unicode, str
    or unicode)
    """
    try:
        result = (Articles(filename), None)
    except Exception as exception:
        result = (filename, str(exception))
    return result
