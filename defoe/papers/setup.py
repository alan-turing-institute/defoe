"""
Map an RDD of filenames into an RDD of defoe.papers.issue.Issue.
"""

from defoe.papers.issue import Issue


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of defoe.papers.issue.Issue.

    :param filenames: RDD of filenames
    :type filenames: pyspark.rdd.RDD
    :return: RDD of defoe.papers.papers.Issue
    :rtype: pyspark.rdd.RDD
    """
    issues = filenames.map(Issue)
    return issues
