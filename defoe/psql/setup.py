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
    fields=lines[1].split(",")
    #host,port,database,user,driver,table
    #ati-nid00006,55555,defoe_db,rfilguei2,org.postgresql.Driver,publication_page
    host=fields[0]
    port=fields[1]
    database=fields[2]
    user=fields[3]
    driver=fields[4]
    table=fields[5]
    sqlContext = SQLContext(context)
    url='postgresql://%s:%s/%s'%(host,port,database)
    properties={'user': user, 'driver': driver}
    df = DataFrameReader(sqlContext).jdbc(url='jdbc:%s' % url, table=table, properties=properties)
    return df
