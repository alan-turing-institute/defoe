"""
Map an RDD of filenames into an RDD of defoe.papers.issue.Issue.
"""

from defoe.papers.issue import Issue


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of defoe.papers.issue.Issue.

    :param filenames: RDD of filenames
    :type filenames: pyspark.rdd.RDD
    :return: RDD of tuples of form (defoe.papers.papers.Issue,
    filename, None) and (None, filename, error message)
    :rtype: tuple(pyspark.rdd.RDD, str or unicode, str or unicode)
    """
    issues = filenames.map(
        lambda filename: create_issue(filename))
    return issues


def create_issue(filename):
    """
    Create an Issue from a filename. If an error arises during its
    creation this is caught and returned.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (defoe.papers.papers.Issue,
    filename, None) or (None, filename, error message)
    :rtype: tuple(pyspark.rdd.RDD, str or unicode, str or unicode)
    """
    try:
        result = (Issue(filename), filename, None)
    except Exception as exception:
        result = (None, filename, str(exception))
    return result
