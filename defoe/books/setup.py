"""
Map an RDD of filenames into an RDD of defoe.books.archive.Archive.
"""

from defoe.books.archive import Archive


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of defoe.books.archive.Archive.

    :param filenames: RDD of filenames
    :type filenames: pyspark.rdd.RDD
    :return: RDD of defoe.books.archive.Archive
    :rtype: pyspark.rdd.RDD
    """
    archives = filenames.map(Archive)
    return archives
