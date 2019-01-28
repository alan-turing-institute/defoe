"""
Given a filename create a defoe.papers.issue.Issue.
"""

from defoe.papers.issue import Issue


def filename_to_object(filename):
    """
    Given a filename create a defoe.papers.issue.Issue.  If an error
    arises during its creation this is caught and returned as a
    string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Issue, None) or (filename, error message),
    if there was an error creating Issue
    :rtype: tuple(defoe.papers.issue.Issue | str or unicode, str or unicode)
    """
    try:
        result = (Issue(filename), None)
    except Exception as exception:
        result = (filename, str(exception))
    return result
