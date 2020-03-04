"""
Given a filename create a defoe.books.archive.Archive.
"""

from defoe.nlsArticles.archive import Archive


def filename_to_object(filename):
    """
    Given a filename create a defoe.books.archive.Archive.  If an error
    arises during its creation this is caught and returned as a
    string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Archive, None) or (filename, error message),
    if there was an error creating Archive
    :rtype: tuple(defoe.books.archive.Archive | str or unicode, str or unicode)
    """
    try:
        result = (Archive(filename), None)
    except Exception as exception:
        result = (filename, str(exception))
    return result
