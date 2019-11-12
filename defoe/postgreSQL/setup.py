"""
Given a filename create a dataframe.
"""

from pyspark.sql import SQLContext
from pyspark.sql import DataFrameReader


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

    lines=open(filename).readlines()
    sqlContext = SQLContext(context)
    url='postgresql://ati-nid00006:55555/defoe_db'
    properties={'user': 'rfilguei2', 'driver': 'org.postgresql.Driver'}
    dbtable="publication_page"
    df = DataFrameReader(sqlContext).jdbc(url='jdbc:%s' % url, table=dbtable , properties=properties)
    return df
