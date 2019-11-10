"""
Given a filename create a defoe.books.archive.Archive.
"""

from pyspark.sql import SQLContext


def filename_to_object(filename, context):
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

    data=open(filename).readline().rstrip()
    sqlContext = SQLContext(context)
    df= sqlContext.read.csv(data, header="true")
    return df
