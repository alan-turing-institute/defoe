"""
Map an RDD of filenames into an RDD of defoe.fmp.archive.Archive.
"""

from defoe.fmp.archive import Archive


def filenames_to_objects(filenames):
    """
    Map an RDD of filenames into an RDD of defoe.fmp.archive.Archive.

    :param filenames: RDD of filenames
    :type filenames: pyspark.rdd.RDD
    :return: RDD of defoe.fmp.archive.Archive
    :rtype: pyspark.rdd.RDD
    """
    archives = filenames.map(Archive)
    return archives
