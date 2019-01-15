"""
Map an RDD of filenames into an RDD of Archive.
"""

from defoe.fmp.archive import Archive


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of Archive.
    """
    archives = filenames.map(Archive)
    return archives
