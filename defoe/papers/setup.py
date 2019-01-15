"""
Map an RDD of filenames into an RDD of Issue.
"""

from defoe.papers.issue import Issue


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of Issue.
    """
    issues = filenames.map(Issue)
    return issues
